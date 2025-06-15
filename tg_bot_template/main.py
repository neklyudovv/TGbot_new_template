import os
import sys
import asyncio
from aiogram.utils.executor import start_polling

def run_tests():
    import pytest
    tests = pytest.main(["-v", "tg_bot_template/tests"])
    if tests != 0:
        sys.exit(tests)

from . import dp
from .config.settings import settings
from .presentation.setup import setup_filters
from .infrastructure.scheduler import bot_scheduler
from .infrastructure.db.connection import setup_db

setup_filters(dp)

async def on_startup(_):
    setup_db(settings)
    asyncio.create_task(bot_scheduler())

from .presentation.handlers import base
from .presentation.handlers import errors
from .presentation.handlers import game
from .presentation.handlers import menu
from .presentation.handlers import profile
from .presentation.handlers import service

def main():
    if os.environ.get("RUN_TESTS") == "true":
        run_tests()
    start_polling(dp, skip_updates=True, on_startup=on_startup)

if __name__ == "__main__":
    main()
