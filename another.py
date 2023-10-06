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


def kb_1():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = KeyboardButton('Посмотреть товары')
    btn_2 = KeyboardButton('Сделать заказ')
    btn_3 = KeyboardButton('Удалить заказ')
    btn_4 = KeyboardButton('Посмотреть заказы')
    keyboard.add(btn_1, btn_2, btn_3, btn_4)
    return keyboard


initial_products = ['яблоки', 'груши', 'апельсины', 'киви', 'бананы', 'ананас']

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL )''')

for product in initial_products:
    cursor.execute('''INSERT INTO products (name) VALUES (?)''', (product,))

conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER,
                name TEXT NOT NULL,
                count INTEGER NOT NULL)''')
conn.commit()


class OrderState(StatesGroup):
    enter_product_name = State()
    enter_product_count = State()
    delete_order = State()


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Здравствуйте, выберите действие', reply_markup=kb_1())


@dp.message_handler(text='Посмотреть товары', state='*')
async def show_products(message: types.Message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT name FROM products''')
    products = cursor.fetchall()
    products_list = sorted(list(set([product[0] for product in products])))
    await message.answer('\n'.join(products_list))


@dp.message_handler(text='Сделать заказ')
async def create_order(messahe: types.Message):
    await messahe.answer('Введите название товара')
    await OrderState.enter_product_name.set()


@dp.message_handler(state=OrderState.enter_product_name)
async def process_product_name(message: types.Message, state: FSMContext):
    product = message.text.lower()
    cursor.execute('''SELECT name FROM products''')
    products = cursor.fetchall()
    products_list = list(set([product_1[0] for product_1 in products]))
    if product not in products_list:
        await message.answer('Такого товара нет в списке')
        return
    async with state.proxy() as data:
        data['product_name'] = product
    await message.answer(f'Введи кол-во товара {data["product_name"]}')
    await OrderState.next()


@dp.message_handler(state=OrderState.enter_product_count)
async def process_product_count(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введите число!')
        return
    async with state.proxy() as data:
        product_name = data["product_name"]
        product_count = message.text
        cursor.execute('''SELECT id FROM products WHERE name=?''', (product_name,))
        product = cursor.fetchone()
        user_id = message.from_user.id
        cursor.execute('''INSERT INTO orders (user_id, name, count) VALUES (?, ?, ?)''',
                       (user_id, product_name, product_count))
        conn.commit()
        await message.answer('Ваш заказ в обработке')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
