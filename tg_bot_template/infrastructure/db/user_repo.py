from datetime import datetime
from aiocache import cached
from aiocache.serializers import PickleSerializer

from .connection import get_db_conn
from tg_bot_template.domain.services.feature_base import TgUser
from tg_bot_template.infrastructure.db.models import Users
from tg_bot_template.presentation.states import UserFormData


@cached(ttl=0.2, serializer=PickleSerializer())
async def get_user_for_filters(*, tg_user: TgUser) -> Users | None:
    return await get_user(tg_user=tg_user)


async def get_user(*, tg_user: TgUser) -> Users | None:
    try:
        user = await get_db_conn().get(Users, social_id=tg_user.tg_id)
    except Exception:
        return None
    else:
        user.username = tg_user.username
        await get_db_conn().update(user)
        return user  # type: ignore[no-any-return]


async def create_user(*, tg_user: TgUser) -> None:
    await get_db_conn().create(
        Users, social_id=tg_user.tg_id, username=tg_user.username, registration_date=datetime.now()
    )


async def update_user_info(*, tg_user: TgUser, user_form_data: UserFormData) -> None:
    user = await get_user(tg_user=tg_user)
    if user is not None:
        user.name = user_form_data.name
        user.info = user_form_data.info
        user.photo = user_form_data.photo
        await get_db_conn().update(user)


async def incr_user_taps(*, tg_user: TgUser) -> None:
    user = await get_user(tg_user=tg_user)
    if user is not None:
        user.taps += 1
        await get_db_conn().update(user)


async def get_all_users() -> list[Users]:
    return list(await get_db_conn().execute(Users.select().order_by(Users.taps.desc())))


