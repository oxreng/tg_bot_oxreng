from config import Config
import logging
from contextlib import suppress
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import BotCommandScopeDefault, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from filters import AdminFilter
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from random import randint
import re

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

secret_num = None
attempts = None


def random_num():
    return randint(1, 10)


def kb():
    start_menu = InlineKeyboardMarkup(resize_keyboard=True)
    button_start = InlineKeyboardButton('Начать', callback_data='start_game')
    button_stop = InlineKeyboardButton('Отмена', callback_data='cancel')
    start_menu.add(button_start, button_stop)
    return start_menu


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer('Привет, это игра "Угадай число"', reply_markup=kb())


@dp.callback_query_handler(text='cancel')
async def end_game(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()


@dp.callback_query_handler(text='start_game')
async def start_game(call: types.CallbackQuery):
    global secret_num, attempts
    attempts = 3
    secret_num = random_num()
    await call.message.answer('Я загадал число от 1 до 10, попробуй отгадать')
    await call.answer()
    await call.message.delete()
    print(secret_num)


@dp.message_handler(regexp=re.compile(r'^\d+$'))
async def check_numbers(message: types.Message):
    global secret_num, attempts
    user_number = int(message.text)
    attempts -= 1
    if secret_num != None:
        if user_number > secret_num:
            await message.reply(f'Ты не угадал! Моё число меньше, оставшееся кол-во попыток {attempts}')
        elif user_number < secret_num:
            await message.reply(f'Ты не угадал! Моё число больше, оставшееся кол-во попыток {attempts}')
        else:
            await message.reply(f'Ты угадал! Поздравляю!!! Начать заново?', reply_markup=kb())
            secret_num = None
            attempts = None
    else:
        await message.reply('Для начала игры нажмите старт')
    if attempts < 1:
        await message.reply('Вы проиграли', reply_markup=kb())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
