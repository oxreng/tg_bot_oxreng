from config import Config
import logging
import sqlite3
from contextlib import suppress
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import BotCommandScopeDefault, BotCommand, InlineKeyboardButton, \
    InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from filters import AdminFilter
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from random import randint
import re
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'Привет user {message.from_user.username}')


@dp.message_handler(text='плохое слово')
async def del_message(message: types.Message):
    await message.delete()


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def banned_member(message: types.Message):
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f'{message.left_chat_member.get_mention(as_html=True)} вышел из чата.')
    elif message.from_user.id == 808197002:  # bot.get_me()
        return
    else:
        await message.reply(f'{message.left_chat_member.full_name} был удалён юзером {message.from_user.full_name}')


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_members(message: types.Message):
    await message.reply(f'Привет {message.new_chat_members[0].full_name}, добро пожаловать в чат, у нас не ругаются')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
