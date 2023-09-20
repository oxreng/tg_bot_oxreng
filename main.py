from config import Config
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from keyboards import kb_drink, kb_start, kb_zak

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет, лови мой ассортимент!', reply_markup=kb_start)


@dp.message_handler(lambda message: message.text.lower().startswith('закуски'))
async def zak_list(message: types.Message):
    await message.answer('Держи все закуски из моего справочника!', reply_markup=kb_zak)


@dp.message_handler(lambda message: message.text.lower().startswith('напитки'))
async def drink_list(message: types.Message):
    await message.answer('Держи все напитки из моего справочника!', reply_markup=kb_drink)


@dp.message_handler(lambda message: message.text.lower().startswith('назад'))
async def back(message: types.Message):
    await message.answer('Хорошо, возвращаюсь в начальное меню', reply_markup=kb_start)


@dp.message_handler()
async def another_answer(message: types.Message):
    await message.answer('Отстань от меня пж, пж, пж....')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
