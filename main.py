from config import Config
import logging
from contextlib import suppress
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import BotCommandScopeDefault, BotCommand, ReplyKeyboardMarkup, KeyboardButton
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


async def set_default_command(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('menu', 'Вывести меню'),
            BotCommand('help', 'Помощь'),
            BotCommand('support', 'Поддержка')
        ],
        scope=BotCommandScopeDefault()
    )


def get_simple_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_1 = KeyboardButton('1')
    btn_2 = KeyboardButton('2')
    kb.row(btn_1, btn_2)
    return kb


def get_simple_kb_1():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_1 = KeyboardButton('Направо')
    btn_2 = KeyboardButton('Налево')
    kb.row(btn_1, btn_2)
    return kb


def get_simple_kb_2():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_1 = KeyboardButton('Вверх')
    btn_2 = KeyboardButton('Вниз')
    kb.row(btn_1, btn_2)
    return kb


def get_simple_kb_back():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_1 = KeyboardButton('На шаг назад')
    btn_2 = KeyboardButton('В главное меню')
    kb.row(btn_1, btn_2)
    return kb


def get_simple_kb_to_main():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_1 = KeyboardButton('В главное меню')
    kb.row(btn_1)
    return kb


@dp.message_handler(commands='start')
async def menu_bot(message: types.Message):
    await message.answer('Привет, держи клаву', reply_markup=get_simple_kb())


@dp.message_handler(text='1')
async def btn1_bot(message: types.Message):
    await message.answer('Вы нажали 1', reply_markup=get_simple_kb_1())


@dp.message_handler(text='2')
async def btn2_bot(message: types.Message):
    await message.answer('Вы нажали 2', reply_markup=get_simple_kb_2())


@dp.message_handler(text='Вверх')
async def btn_up_bot(message: types.Message):
    await message.answer('Вы нажали вверх', reply_markup=get_simple_kb_back())


@dp.message_handler(text='Вниз')
async def btn_down_bot(message: types.Message):
    await message.answer('Вы нажали вниз', reply_markup=get_simple_kb_back())


@dp.message_handler(text='Направо')
async def btn_r_bot(message: types.Message):
    await message.answer('Вы нажали направо', reply_markup=get_simple_kb_back())


@dp.message_handler(text='Налево')
async def btn_l_bot(message: types.Message):
    await message.answer('Вы нажали налево', reply_markup=get_simple_kb_back())


@dp.message_handler(text='В главное меню')
async def btn_r_bot(message: types.Message):
    await message.answer('Вы вышли в главное меню', reply_markup=get_simple_kb())


@dp.message_handler(text='На шаг назад')
async def btn_l_bot(message: types.Message):
    await message.answer('Вы вышли на шаг назад', reply_markup=get_simple_kb_2())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
