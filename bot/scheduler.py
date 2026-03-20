import asyncio
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.checker import build_check_url, check_status
from bot.database import get_all_cases, update_case_status
from bot.locale import t

logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 6 * 60 * 60  # 6 hours
FIRST_CHECK_DELAY = 5  # seconds after bot start
REQUEST_DELAY = 1.0  # delay between requests to avoid overloading the server


async def check_all_statuses(context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Starting scheduled status check")
    cases = await get_all_cases()
    logger.info("Checking %d cases", len(cases))

    for case in cases:
        case_number = case["case_number"]
        lang = case["language"]
        chat_id = case["chat_id"]
        old_status = case["last_status"]

        new_status = await check_status(case_number, lang)
        if new_status is None:
            logger.warning("Failed to check case %s", case_number)
            continue

        await update_case_status(case["id"], new_status)

        if new_status != old_status:
            try:
                url = build_check_url(case_number, lang)
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(t(lang, "btn_check_website"), url=url)]
                ])
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=t(lang, "status_changed", case=case_number, status=new_status),
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard,
                )
                logger.info("Notified user %s about case %s change", case["user_id"], case_number)
            except Exception:
                logger.exception("Failed to send notification to chat %s", chat_id)

        await asyncio.sleep(REQUEST_DELAY)

    logger.info("Scheduled status check complete")


def schedule_jobs(application) -> None:
    job_queue = application.job_queue
    job_queue.run_repeating(
        check_all_statuses,
        interval=CHECK_INTERVAL_SECONDS,
        first=FIRST_CHECK_DELAY,
        name="status_check",
    )
    logger.info("Scheduled status check every %d hours", CHECK_INTERVAL_SECONDS // 3600)
