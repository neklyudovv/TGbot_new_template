from typing import Any

from aiogram import types
from aiogram.dispatcher.filters import Text

from ... import dp
from . import feature_config as features
from tg_bot_template.infrastructure.tg.callbacks import game_cb
from tg_bot_template.domain.services.feature_base import Feature, InlineButton, TgUser
from tg_bot_template.infrastructure.tg.utils import bot_edit_callback_message, bot_safe_send_photo
from tg_bot_template.infrastructure.db import user_repo


@dp.message_handler(Text(equals=features.rating_ftr.triggers, ignore_case=True), registered=True)
async def rating(msg: types.Message) -> None:
    user = await user_repo.get_user(tg_user=TgUser(tg_id=msg.from_user.id, username=msg.from_user.username))
    all_users = await user_repo.get_all_users()
    total_taps = sum([i.taps for i in all_users])
    text = features.rating_ftr.text.format(user_taps=user.taps, total_taps=total_taps)  # type: ignore[union-attr]
    await msg.answer(text, reply_markup=features.rating_ftr.kb)
    if all_users and (best_user := all_users[0]).taps > 0:
        text = features.rating_ftr.text2.format(  # type: ignore[union-attr]
            name=best_user.name, username=best_user.username, info=best_user.info
        )
        await msg.answer(text, reply_markup=features.rating_ftr.kb)
        await bot_safe_send_photo(dp, msg.from_user.id, best_user.photo, reply_markup=features.rating_ftr.kb)


@dp.message_handler(Text(equals=features.press_button_ftr.triggers, ignore_case=True), registered=True)
async def send_press_button(msg: types.Message) -> None:
    text, keyboard = await update_button_tap(taps=0)
    await msg.answer(text, reply_markup=Feature.create_tg_inline_kb(keyboard))


@dp.callback_query_handler(game_cb.filter(action=features.press_button_ftr.callback_action), registered=True)
async def count_button_tap(callback: types.CallbackQuery, callback_data: dict[Any, Any]) -> None:
    current_taps = int(callback_data["taps"])
    new_taps = current_taps + 1
    await user_repo.incr_user_taps(tg_user=TgUser(tg_id=callback.from_user.id, username=callback.from_user.username))
    text, keyboard = await update_button_tap(taps=new_taps)
    await bot_edit_callback_message(dp, callback, text, reply_markup=Feature.create_tg_inline_kb(keyboard))


async def update_button_tap(*, taps: int) -> tuple[str, list[list[InlineButton]]]:
    text = features.press_button_ftr.text.format(last_session=taps)  # type: ignore[union-attr]
    keyboard = [
        [
            InlineButton(
                text=features.press_button_ftr.button,
                callback_data=game_cb.new(action=features.press_button_ftr.callback_action, taps=taps),
            )
        ],
        [
            InlineButton(
                text=features.start_ftr.button,
                callback_data=game_cb.new(action=features.start_ftr.callback_action, taps=taps),
            )
        ],
    ]
    return text, keyboard