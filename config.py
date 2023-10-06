class Config:
    TOKEN = '6378931392:AAFLqQ6hEqwM2BAhdXNq32LwTiwp4vb1jRk'
    KEY = 'c465369b9521e340aa8cf1965beadec3'
    SUPER_USER_IDS = '808197002'


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
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

conn = sqlite3.connect('tests_answers.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS answers 
                ( user_id INTEGER PRIMARY KEY, 
                answer TEXT )''')


class AnwerStatr(StatesGroup):
    enter_test = State()


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await set_default_commands(dp)
    await message.answer('Здравствуйте, напишите /help для помощи')


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            BotCommand('start', 'Запустить тест'),
            BotCommand('help', 'Вывести справку'),
            BotCommand('test', 'Пройти тест'),
            BotCommand('del_my_ans', 'Удалить вас из БД')
        ]
    )


@dp.message_handler(commands='help', state='*')
async def help_me(message: types.Message, state: FSMContext):
    await message.reply('Напишите /test для прохождения опроса и /del_my_ans '
                        'для повторного прохождения опроса')


@dp.message_handler(commands='test', state='*')
async def test_start(message: types.Message, state: FSMContext):
    users = list(cursor.execute('''SELECT user_id FROM answers''').fetchall())
    if message.from_user.id not in users:
        await message.answer('Назовите ваш любимый фильм.')
        await AnwerStatr.enter_test.set()
    else:
        await message.answer('Вы уже учавствовали в опросе!')


@dp.message_handler(commands='del_my_ans', state='*')
async def del_me(message: types.Message, state: FSMContext):
    cursor.execute('''DELETE FROM answers WHERE user_id = ?''', (message.from_user.id,))
    conn.commit()


@dp.message_handler(state=AnwerStatr.enter_test)
async def answer(message: types.Message, state: FSMContext):
    cursor.execute('''INSERT INTO answers (user_id, answer) VALUES (?, ?)''', (message.from_user.id, message.text))
    conn.commit()
    await state.finish()
    await message.answer('Спасибо за прохождение опроса!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
