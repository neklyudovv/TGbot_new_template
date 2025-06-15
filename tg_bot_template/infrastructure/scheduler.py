import asyncio
import aioschedule
from loguru import logger

from ..config.settings import settings
from .tg.utils import bot_safe_send_message
from .. import dp

async def healthcheck():
    logger.info("Healthcheck ping")
    if settings.creator_id:
        await bot_safe_send_message(dp, settings.creator_id, "✅ Бот работает")

async def bot_scheduler():
    logger.info("Scheduler started")
    aioschedule.every().day.at(settings.schedule_healthcheck).do(healthcheck)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
