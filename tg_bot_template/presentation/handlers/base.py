from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from ... import dp
from .menu import main_menu
from . import feature_config as features
from tg_bot_template.infrastructure.tg.callbacks import game_cb
from tg_bot_template.infrastructure.tg.utils import bot_edit_callback_message, bot_safe_send_message


@dp.message_handler(lambda message: features.ping_ftr.find_triggers(message))
async def ping(msg: types.Message) -> None:
    await bot_safe_send_message(dp, msg.from_user.id, features.ping_ftr.text)  # type: ignore[arg-type]


@dp.message_handler(lambda message: features.creator_ftr.find_triggers(message), creator=True)
async def creator_filter_check(msg: types.Message) -> None:
    await msg.answer(features.creator_ftr.text, parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(Text(equals=features.cancel_ftr.triggers, ignore_case=True), state="*")
async def cancel_command(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(features.cancel_ftr.text)
    if await state.get_state() is not None:
        await state.finish()
    await main_menu(from_user_id=msg.from_user.id)


@dp.callback_query_handler(Text(equals=features.cancel_ftr.triggers, ignore_case=True), state="*")
async def cancel_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot_edit_callback_message(dp, callback, features.cancel_ftr.text)
    if await state.get_state() is not None:
        await state.finish()
    await main_menu(from_user_id=callback.from_user.id)


@dp.callback_query_handler(game_cb.filter(action=features.start_ftr.callback_action), registered=True)
@dp.message_handler(Text(equals=features.start_ftr.triggers, ignore_case=True), registered=True)
async def start(msg: types.Message | types.CallbackQuery) -> None:
    await main_menu(from_user_id=msg.from_user.id)
    if isinstance(msg, types.CallbackQuery):
        await msg.answer()


@dp.message_handler(Text(equals=features.help_ftr.triggers, ignore_case=True), registered=True)
async def help_feature(msg: types.Message) -> None:
    await msg.answer(features.help_ftr.text, reply_markup=features.empty.kb)



