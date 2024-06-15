from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import SimpleEventIsolation

from src.database.cache_db import TG_STORAGE
from src.utils.config import TELEGRAM_API_TOKEN

bot = Bot(token=TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=TG_STORAGE, events_isolation=SimpleEventIsolation())