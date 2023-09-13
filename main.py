from config import Config
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

link_regexp = r'https://\S+$'


@dp.message_handler(filters.Regexp(link_regexp))
async def regexp_example(message: types.Message):
    await message.answer('О, ссылка')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
