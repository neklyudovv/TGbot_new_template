from ... import dp
from . import feature_config as features
from tg_bot_template.infrastructure.tg.utils import bot_safe_send_message


async def main_menu(*, from_user_id: int) -> None:
    text = f"{features.start_ftr.text}\n\n{features.start_ftr.menu.text}"  # type: ignore[union-attr]
    await bot_safe_send_message(dp, from_user_id, text, reply_markup=features.start_ftr.kb)