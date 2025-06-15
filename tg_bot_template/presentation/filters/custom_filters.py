from aiogram import types

from tg_bot_template.infrastructure.tg.aiogram_ext import AbsFilter
from tg_bot_template.domain.services.feature_base import TgUser
from tg_bot_template.config.settings import settings
from tg_bot_template.domain.services.user_service import check_user_registered


class CreatorFilter(AbsFilter):
    key = "creator"

    async def check(self, msg: types.Message) -> bool:
        return settings.creator_id is None or msg.from_user.id == settings.creator_id


class RegistrationFilter(AbsFilter):
    key = "registered"

    async def check(self, msg: types.Message) -> bool:
        return await check_user_registered(tg_user=TgUser(tg_id=msg.from_user.id, username=msg.from_user.username))


class NonRegistrationFilter(AbsFilter):
    key = "not_registered"

    async def check(self, msg: types.Message) -> bool:
        return not await check_user_registered(tg_user=TgUser(tg_id=msg.from_user.id, username=msg.from_user.username))
