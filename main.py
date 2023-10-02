from config import Config
import logging
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

food_names = ['суши', 'паста', 'устрицы', 'лагман']
food_size = ['маленькую', 'среднюю', 'большую']


class OrderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('выберите что хотите заказать /food, /drinks', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands='cancel', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('действие отменено', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands='food', state='*')
async def food_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in food_names:
        kb.add(name)
    await message.answer('Выберите блюдо', reply_markup=kb)
    await OrderFood.waiting_for_food_name.set()


@dp.message_handler(state=OrderFood.waiting_for_food_name)
async def food_choise(message: types.Message, state: FSMContext):
    if message.text.lower() not in food_names:
        await message.answer('Пожалуйста, выбери блюдо с клавиатуры')
        return
    await state.update_data(food_choise=message.text.lower())

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for size in food_size:
        kb.add(size)
    await OrderFood.next()
    await message.answer('Выберите порцию', reply_markup=kb)


@dp.message_handler(state=OrderFood.waiting_for_food_size)
async def size_choise(message: types.Message, state: FSMContext):
    if message.text.lower() not in food_size:
        await message.answer('Пожалуйста, выберите порцию с клавиатуры')
        return
    user_data = await state.get_data()
    await message.answer(f'Вы заказали {message.text.lower()} порцию {user_data["food_choise"]}'
                         f'\nПопробуйте теперь заказать напитки', reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
