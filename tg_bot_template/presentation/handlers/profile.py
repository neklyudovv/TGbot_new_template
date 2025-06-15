from typing import Type

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup

from ... import dp
from . import feature_config as features
from .errors import Errors
from ..states import UserForm, UserFormData
from tg_bot_template.domain.services.feature_base import Feature, TgUser
from tg_bot_template.infrastructure.db import user_repo


@dp.message_handler(Text(equals=features.set_user_info.triggers, ignore_case=True), registered=True)
async def set_name(msg: types.Message) -> None:
    await msg.answer(features.set_user_info.text, reply_markup=features.cancel_ftr.kb)
    await UserForm.name.set()


@dp.message_handler(content_types=["text", "caption"], state=UserForm.name)
async def add_form_name(msg: types.Message, state: FSMContext) -> None:
    await fill_form(msg=msg, feature=features.set_user_name, form=UserForm, state=state)


@dp.message_handler(content_types=["text", "caption"], state=UserForm.info)
async def add_form_info(msg: types.Message, state: FSMContext) -> None:
    await fill_form(msg=msg, feature=features.set_user_about, form=UserForm, state=state)


async def fill_form(*, msg: types.Message, feature: Feature, form: Type[StatesGroup], state: FSMContext) -> None:
    async with state.proxy() as data:
        data[feature.data_key] = msg.caption or msg.text
    await form.next()
    await msg.answer(feature.text, reply_markup=features.cancel_ftr.kb)


@dp.message_handler(content_types=["photo"], state=UserForm.photo)
async def add_form_photo(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        user_form_data = UserFormData(
            name=data[features.set_user_name.data_key],
            info=data[features.set_user_about.data_key],
            photo=msg.photo[-1].file_id,
        )
        tg_user = TgUser(tg_id=msg.from_user.id, username=msg.from_user.username)
        await user_repo.update_user_info(tg_user=tg_user, user_form_data=user_form_data)
    await state.finish()
    await msg.answer(features.set_user_info.text2, reply_markup=features.set_user_info.kb)


@dp.message_handler(content_types=["any"], state=UserForm.name)
async def error_form_name(msg: types.Message) -> None:
    await msg.answer(Errors.text_form, reply_markup=features.cancel_ftr.kb)


@dp.message_handler(content_types=["any"], state=UserForm.info)
async def error_form_info(msg: types.Message) -> None:
    await msg.answer(Errors.text_form, reply_markup=features.cancel_ftr.kb)


@dp.message_handler(content_types=["any"], state=UserForm.photo)
async def error_form_photo(msg: types.Message) -> None:
    await msg.answer(Errors.photo_form, reply_markup=features.cancel_ftr.kb)