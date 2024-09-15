from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage

# TODO Move to env
REDIS_URL = "redis://localhost:6379/2"

TG_STORAGE = RedisStorage.from_url(REDIS_URL, key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True))
