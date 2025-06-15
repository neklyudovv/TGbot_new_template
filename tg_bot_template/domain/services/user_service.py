from tg_bot_template.infrastructure.db.user_repo import get_user_for_filters
from tg_bot_template.domain.services.feature_base import TgUser


async def check_user_registered(tg_user: TgUser) -> bool:
    user = await get_user_for_filters(tg_user=tg_user)
    return bool(user)