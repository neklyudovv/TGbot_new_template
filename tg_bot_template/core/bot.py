import asyncio

import aioschedule
from aiogram import types
from loguru import logger

from .. import dp
from tg_bot_template.presentation.handlers import feature_config as features
from tg_bot_template.infrastructure.tg.aiogram_ext import DbDispatcher
from tg_bot_template.domain.services.feature_base import Feature
from tg_bot_template.infrastructure.tg.utils import bot_safe_send_message
from ..config.settings import settings


async def healthcheck() -> None:
    logger.info(features.ping_ftr.text2)
    if settings.creator_id is not None:
        await bot_safe_send_message(dp, int(settings.creator_id), features.ping_ftr.text2)  # type: ignore[arg-type]


async def bot_scheduler() -> None:
    logger.info("Scheduler is up")
    aioschedule.every().day.at(settings.schedule_healthcheck).do(healthcheck)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher: DbDispatcher) -> None:
    logger.info("Bot is up")
    await bot_safe_send_message(dp, settings.creator_id, "Bot is up")

    # bot commands setup
    cmds = Feature.commands_to_set
    bot_commands = [types.BotCommand(ftr.slashed_command, ftr.slashed_command_descr) for ftr in cmds]
    await dispatcher.bot.set_my_commands(bot_commands)

    # scheduler startup
    await asyncio.create_task(bot_scheduler())


async def on_shutdown(dispatcher: DbDispatcher) -> None:
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
