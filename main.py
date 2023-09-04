from aiogram import Dispatcher, Bot, types, executor
import logging
from random import choice
from config import Config

# Заходим в bash на dashboard, потом пишем ls,
# заходим в нужную папку (cd ...) и пишем python и название файла

TOKEN = Config.TOKEN
HELLO_LIST = ['Welcome,', 'I’m glad to see you,', 'Hello there,',
              'Bonjour,', 'Buenos días,', 'Olá,', 'Hallo,']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# Основные команды - git status - все изменения
# Основные команды - git push

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply(f'{choice(HELLO_LIST)} {message.chat.first_name}!')


@dp.message_handler(commands='about')
async def cmd_start(message: types.Message):
    await message.reply("Hi! I am a bot to whom you can write any message! "
                        "Don't forget to check /start!")


@dp.message_handler()
async def cmd_start(message: types.Message):
    await message.answer(f'Why you said "{message.text}"?')


if __name__ == '__main__':
    executor.start_polling(dp)
