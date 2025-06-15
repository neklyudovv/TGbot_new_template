import pytest
import asyncio

import tg_bot_template.infrastructure.db.connection as db_conn_module
from tg_bot_template.domain.services.user_service import check_user_registered
from tg_bot_template.domain.services.feature_base import TgUser
from tg_bot_template.infrastructure.db.models import Users

@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
def setup_test_db():
    new_settings = db_conn_module.settings.__class__()
    manager = db_conn_module.setup_db(new_settings)

    yield manager

@pytest.mark.asyncio
async def test_check_user_registered_returns_false_for_unregistered(setup_test_db):
    tg_user = TgUser(tg_id=123456789, username="not_registered")
    registered = await check_user_registered(tg_user)
    assert registered is False

@pytest.mark.asyncio
async def test_check_user_registered_returns_true_for_registered(setup_test_db):
    tg_user = TgUser(tg_id=987654321, username="registered_user")

    await setup_test_db.create(
        Users,
        social_id=tg_user.tg_id,
        username=tg_user.username,
        registration_date=None
    )

    registered = await check_user_registered(tg_user)
    assert registered is True
