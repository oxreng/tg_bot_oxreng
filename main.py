from config import Config
import logging
from contextlib import suppress
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import BotCommandScopeDefault, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters import AdminFilter
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from random import randint
import re

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())
user_data = {}


def get_keyboard():
    buttons = [types.InlineKeyboardButton(text='-1', callback_data='num_decr'),
               types.InlineKeyboardButton(text='+1', callback_data='num_incr'),
               types.InlineKeyboardButton(text='Подтвердить', callback_data='num_finish')]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value):
    await message.edit_text(f'Укажите число: {new_value}', reply_markup=get_keyboard())


@dp.message_handler(commands='numbers')
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer('Укажите число: 0', reply_markup=get_keyboard())


@dp.callback_query_handler(lambda callback_query: re.match(r'^num_.{0,10}$', callback_query.data))
async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    action = call.data.split('_')[1]
    if action == 'incr':
        user_data[call.from_user.id] = user_value + 1
        await update_num_text(call.message, user_value + 1)
    elif action == 'decr':
        user_data[call.from_user.id] = user_value - 1
        await update_num_text(call.message, user_value - 1)
    else:
        await call.message.edit_text(f'Итого: {user_value}')
    await call.answer()


@dp.message_handler(commands='random')
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('нажми', callback_data='random_value'))
    await message.answer('Нажми на кнопку, чтобы получить рандомное число', reply_markup=keyboard)


@dp.callback_query_handler(text='random_value')
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))
    await call.answer(text='Спасибо', show_alert=True)  # Отвечает на callback и позв. нажать >= 1  раз


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
#
