# from root.settings import API_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

API_TOKEN = '1841108890:AAER2-O1tZRZdVJnWJdfu9lcSHs2TFQaFy0'
bot = Bot(API_TOKEN)
redis_storage = RedisStorage2()
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)
