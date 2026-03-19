import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.database import init_db
from bot.handlers import (
    language_callback,
    menu_add_callback,
    menu_help_callback,
    menu_language_callback,
    menu_main_callback,
    menu_remove_callback,
    menu_status_callback,
    remove_callback,
    start_command,
    text_message_handler,
)
from bot.scheduler import schedule_jobs

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def post_init(application) -> None:
    await init_db()
    schedule_jobs(application)
    logger.info("Bot initialized")


def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")

    application = (
        ApplicationBuilder()
        .token(token)
        .post_init(post_init)
        .build()
    )

    # Commands
    application.add_handler(CommandHandler("start", start_command))

    # Inline button callbacks
    application.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang_"))
    application.add_handler(CallbackQueryHandler(menu_main_callback, pattern=r"^menu_main$"))
    application.add_handler(CallbackQueryHandler(menu_add_callback, pattern=r"^menu_add$"))
    application.add_handler(CallbackQueryHandler(menu_status_callback, pattern=r"^menu_status$"))
    application.add_handler(CallbackQueryHandler(menu_remove_callback, pattern=r"^menu_remove$"))
    application.add_handler(CallbackQueryHandler(menu_language_callback, pattern=r"^menu_language$"))
    application.add_handler(CallbackQueryHandler(menu_help_callback, pattern=r"^menu_help$"))
    application.add_handler(CallbackQueryHandler(remove_callback, pattern=r"^rm_"))

    # Text messages (for add flow)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))

    logger.info("Starting bot")
    asyncio.set_event_loop(asyncio.new_event_loop())
    application.run_polling()


if __name__ == "__main__":
    main()
