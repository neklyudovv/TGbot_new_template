import asyncio
from aiogram.utils.executor import start_polling

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



if __name__ == "__main__":
    start_polling(dp, skip_updates=True, on_startup=on_startup)
