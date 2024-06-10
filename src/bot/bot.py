import asyncio

from src.bot import bot, dp
from src.bot.handlers.category import category_router
from src.bot.handlers.main_menu import main_menu_router
from src.bot.handlers.setting import settings_router
from src.bot.handlers.statistics import statistics_router
from src.database import init_db


async def start_bot() -> None:
    await init_db()

    # Register routers
    dp.include_router(main_menu_router)
    dp.include_router(settings_router)
    dp.include_router(statistics_router)
    dp.include_router(category_router)

    await dp.start_polling(bot)


asyncio.run(start_bot())
