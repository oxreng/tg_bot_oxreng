import asyncio
import sqlite3
import logging
from config import Config
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

# Заходим в bash на dashboard, потом пишем ls,
# заходим в нужную папку (cd ..) и пишем python и название файла

TOKEN = Config.TOKEN
WEBHOOK_HOST = 'https://470c-176-120-190-90.ngrok-free.app'
WEBHOOK_PATH = f'/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 8000

loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, loop=loop)
dp = Dispatcher(bot)

db_filename = 'tasks.db'


def create_table():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS tasks
         (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         user_id INTEGER,
         task_text TEXT)'''
    )
    conn.commit()
    conn.close()


create_table()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Здравствуй, юзер!')


@dp.message_handler(lambda message: message.text.startswith('/add_task '))
async def add_task(message: types.Message):
    user_id = message.from_user.id
    task_text = message.text.replace('/add_task ', '')
    if not task_text:
        await message.answer('Введите текст задания!')
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (user_id, task_text) VALUES (?, ?)', (user_id, task_text)
    )
    conn.commit()
    conn.close()
    await message.answer('Задание добавлено успешно!')


@dp.message_handler(commands=['list_tasks'])
async def list_tasks(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    who = list(cursor.execute(
        'SELECT id, task_text FROM tasks WHERE user_id=?', (user_id,)
    ))
    conn.close()
    await message.answer('\n'.join([(': ').join(i) for i in [(str(i[0]), str(i[1])) for i in who]]))


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()


if __name__ == '__main__':
    start_webhook(dispatcher=dp,
                  webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup,
                  on_shutdown=on_shutdown,
                  skip_updates=True,
                  host=WEBAPP_HOST,
                  port=WEBAPP_PORT
                  )
