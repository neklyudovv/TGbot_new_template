import asyncio

from aiogram import types
from aiogram.utils.exceptions import RetryAfter, BotBlocked
from loguru import logger

from ... import dp
from .menu import main_menu
from . import feature_config as features
from .errors import Errors
from tg_bot_template.domain.services.feature_base import TgUser
from tg_bot_template.config.settings import settings
from tg_bot_template.infrastructure.db import user_repo


@dp.message_handler(content_types=["any"], not_registered=True)
async def registration(msg: types.Message) -> types.Message | None:
    if settings.register_passphrase is not None:
        if msg.text.lower() != settings.register_passphrase:
            return await msg.answer(Errors.please_register, reply_markup=features.empty.kb)
        if not msg.from_user.username:
            return await msg.answer(Errors.register_failed, reply_markup=features.empty.kb)
    # user registration
    await user_repo.create_user(tg_user=TgUser(tg_id=msg.from_user.id, username=msg.from_user.username))
    await msg.answer(features.register_ftr.text)
    await main_menu(from_user_id=msg.from_user.id)
    return None


@dp.message_handler(content_types=["any"], registered=True)
async def handle_wrong_text_msg(msg: types.Message) -> None:
    await asyncio.sleep(2)
    await msg.reply(Errors.text)


@dp.my_chat_member_handler()
async def handle_my_chat_member_handlers(msg: types.Message):
    logger.info(msg)  # уведомление о блокировке


@dp.errors_handler(exception=BotBlocked)
async def exception_handler(update: types.Update, exception: BotBlocked):
    # работает только для хендлеров бота, для шедулера не работает
    logger.info(update.message.from_user.id)  # уведомление о блокировке
    logger.info(exception)  # уведомление о блокировке
    return True