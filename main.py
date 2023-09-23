from config import Config
import logging
from contextlib import suppress
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import BotCommandScopeDefault, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
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


def get_menu():
    menu_kb = InlineKeyboardMarkup(row_width=2)
    pizza_button = InlineKeyboardButton(text='Пицца 🍕', callback_data='pizza_cat')
    snacks_button = InlineKeyboardButton(text='Закуски 🍟', callback_data='snacks_cat')
    menu_kb.insert(pizza_button)
    menu_kb.insert(snacks_button)
    return menu_kb


@dp.message_handler(AdminFilter(), CommandStart())
async def admin_start(message: types.Message):
    await message.reply('Команды установлены')
    await set_default_command(message.bot)


@dp.message_handler(commands='menu')
async def menu_bot(message: types.Message):
    await message.answer('Приветсвую! Это доставка еды', reply_markup=get_menu())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
#
