from config import Config
from aiogram.types import ReplyKeyboardRemove
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from keyboards import kb, inline_kb, inline_kb_full
import re

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply('Отправляю кнопку', reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda callback_query: re.match(r'^btn.{0,10}$', callback_query.data))
async def process_callback_kb_full(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    print(code)
    if code.isdigit():
        code = int(code)
    if code == 1:
        await bot.answer_callback_query(callback_query.id, text='Нажата 1 кнопка')
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка {code}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
