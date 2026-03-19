import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.checker import check_status
from bot.database import (
    add_case,
    get_user,
    get_user_cases,
    remove_case,
    set_language,
    upsert_user,
)
from bot.locale import t

logger = logging.getLogger(__name__)

LANGUAGE_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇮🇹 Italiano", callback_data="lang_it"),
    ]
])

NOT_FOUND_MARKERS = [
    "нет в архиве",
    "not found",
    "non presente",
    "non è presente",
]


def _menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t(lang, "btn_add"), callback_data="menu_add"),
            InlineKeyboardButton(t(lang, "btn_status"), callback_data="menu_status"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_remove"), callback_data="menu_remove"),
            InlineKeyboardButton(t(lang, "btn_language"), callback_data="menu_language"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_help"), callback_data="menu_help"),
        ],
    ])


def _back_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu_main")],
    ])


async def _get_lang(user_id: int) -> str | None:
    user = await get_user(user_id)
    return user["language"] if user else None


# ── /start ──────────────────────────────────────────────

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("state", None)
    lang = await _get_lang(update.effective_user.id)
    if lang:
        # User already registered — go straight to menu
        await update.message.reply_text(
            t(lang, "welcome"),
            reply_markup=_menu_keyboard(lang),
            parse_mode=ParseMode.HTML,
        )
        return
    await update.message.reply_text(
        t("en", "choose_language"),
        reply_markup=LANGUAGE_KEYBOARD,
    )


# ── Language selection callback ─────────────────────────

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = query.data.removeprefix("lang_")
    await upsert_user(query.from_user.id, query.message.chat_id, lang)
    await query.edit_message_text(
        t(lang, "language_set") + "\n\n" + t(lang, "welcome"),
        reply_markup=_menu_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )


# ── Menu callbacks ──────────────────────────────────────

async def menu_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data.pop("state", None)
    lang = await _get_lang(query.from_user.id)
    if not lang:
        await query.edit_message_text(t("en", "not_registered"))
        return
    await query.edit_message_text(
        t(lang, "welcome"),
        reply_markup=_menu_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )


async def menu_add_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = await _get_lang(query.from_user.id)
    if not lang:
        await query.edit_message_text(t("en", "not_registered"))
        return
    context.user_data["state"] = "awaiting_add"
    await query.edit_message_text(
        t(lang, "prompt_add"),
        reply_markup=_back_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )


async def menu_status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = await _get_lang(query.from_user.id)
    if not lang:
        await query.edit_message_text(t("en", "not_registered"))
        return

    cases = await get_user_cases(query.from_user.id)
    if not cases:
        await query.edit_message_text(
            t(lang, "no_cases"),
            reply_markup=_menu_keyboard(lang),
            parse_mode=ParseMode.HTML,
        )
        return

    lines = [t(lang, "status_header")]
    for i, case in enumerate(cases, 1):
        checked = case["last_checked_at"] or "—"
        status = case["last_status"] or "—"
        lines.append(t(lang, "status_row", i=i, case=case["case_number"], status=status, checked=checked))
    await query.edit_message_text(
        "\n".join(lines),
        reply_markup=_back_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )


async def menu_remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = await _get_lang(query.from_user.id)
    if not lang:
        await query.edit_message_text(t("en", "not_registered"))
        return

    cases = await get_user_cases(query.from_user.id)
    if not cases:
        await query.edit_message_text(
            t(lang, "no_cases"),
            reply_markup=_menu_keyboard(lang),
            parse_mode=ParseMode.HTML,
        )
        return

    buttons = [
        [InlineKeyboardButton(f"❌ {c['case_number']}", callback_data=f"rm_{c['case_number']}")]
        for c in cases
    ]
    buttons.append([InlineKeyboardButton(t(lang, "btn_menu"), callback_data="menu_main")])
    await query.edit_message_text(
        t(lang, "prompt_remove"),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML,
    )


async def menu_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        t("en", "choose_language"),
        reply_markup=LANGUAGE_KEYBOARD,
    )


async def menu_help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = await _get_lang(query.from_user.id)
    if not lang:
        await query.edit_message_text(t("en", "not_registered"))
        return
    await query.edit_message_text(
        t(lang, "help"),
        reply_markup=_back_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )


# ── Remove case callback ───────────────────────────────

async def remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = await _get_lang(query.from_user.id)
    if not lang:
        return
    case_number = query.data.removeprefix("rm_")
    removed = await remove_case(query.from_user.id, case_number)
    text = t(lang, "case_removed", case=case_number) if removed else t(lang, "case_not_tracked", case=case_number)
    await query.edit_message_text(
        text,
        reply_markup=_menu_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )


# ── Text message handler (for add flow) ────────────────

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = context.user_data.get("state")
    if state != "awaiting_add":
        return

    context.user_data.pop("state", None)
    lang = await _get_lang(update.effective_user.id)
    if not lang:
        await update.message.reply_text(t("en", "not_registered"))
        return

    case_number = update.message.text.strip().upper()
    user_id = update.effective_user.id

    msg = await update.message.reply_text(
        t(lang, "checking", case=case_number),
        parse_mode=ParseMode.HTML,
    )

    status = await check_status(case_number, lang)
    if status is None:
        await msg.edit_text(
            t(lang, "check_error", case=case_number),
            reply_markup=_menu_keyboard(lang),
            parse_mode=ParseMode.HTML,
        )
        return

    if any(marker in status.lower() for marker in NOT_FOUND_MARKERS):
        await msg.edit_text(
            t(lang, "case_not_found", case=case_number),
            reply_markup=_menu_keyboard(lang),
            parse_mode=ParseMode.HTML,
        )
        return

    added = await add_case(user_id, case_number, status)
    if not added:
        cases = await get_user_cases(user_id)
        if len(cases) >= 10:
            text = t(lang, "limit_reached")
        else:
            text = t(lang, "case_exists", case=case_number)
        await msg.edit_text(text, reply_markup=_menu_keyboard(lang), parse_mode=ParseMode.HTML)
        return

    await msg.edit_text(
        t(lang, "case_added", case=case_number, status=status),
        reply_markup=_menu_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )
