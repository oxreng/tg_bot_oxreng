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


def get_inline_kb():
    inline_kb = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton('1', callback_data='1'),
            InlineKeyboardButton('2', callback_data='2')]
    inline_kb.add(*btns)
    return inline_kb


def get_inline_kb_1():
    inline_kb = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton('вперед', callback_data='forward'),
            InlineKeyboardButton('закрыть', callback_data='back')]
    inline_kb.add(*btns)
    return inline_kb


@dp.message_handler(commands='start')
async def menu_bot(message: types.Message):
    await message.answer('Это инлайн клава', reply_markup=get_inline_kb())


@dp.callback_query_handler(text='1')
async def btn_1(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Нажата кнопка 1', reply_markup=get_inline_kb_1())


@dp.callback_query_handler(text='back')
async def btn_back(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Вышли в главное меню', reply_markup=get_inline_kb())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
