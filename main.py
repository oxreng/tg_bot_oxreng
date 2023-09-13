from config import Config
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(filters.IDFilter(chat_id=Config.SUPER_USER_IDS))
@dp.message_handler(chat_id = Config.SUPER_USER_IDS)
async def id_filters(message: types.Message):
    await message.answer('Помню я тебя!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
