import sqlite3
from config import Config
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

# Подключаемся
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)''')
conn.commit()


class UserManager:
    @staticmethod
    def is_user_exists(user_id):
        cursor.execute('''SELECT user_id FROM users WHERE user_id = ?''', (user_id,))
        return cursor.fetchone() is not None

    @staticmethod
    def add_user(user_id, username):
        cursor.execute('''INSERT INTO users (user_id, username) VALUES (?, ?)''', (user_id, username))
        conn.commit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
