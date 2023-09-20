from config import Config
from aiogram.types import ReplyKeyboardRemove
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from keyboards import kb

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply('Привет', reply_markup=kb)


@dp.message_handler(commands='rm')
async def cmd_rm(message: types.Message):
    await message.reply('Убрать клавиатуру', reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
