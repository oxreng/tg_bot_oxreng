class Config:
    TOKEN = '6444324425:AAHlxKZsNnBp3GOmUqh5LpUBlYvAqgdoTfI'
    KEY = 'c465369b9521e340aa8cf1965beadec3'
    SUPER_USER_IDS = '808197002'


# from config import Config
# import logging
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# import sqlite3
#
# bot = Bot(token=Config.TOKEN)
# dp = Dispatcher(bot)
# logging.basicConfig(level=logging.INFO)
# dp.middleware.setup(LoggingMiddleware())
#
# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS black_users (user_id INTEGER PRIMARY KEY, reason TEXT)''')
# conn.commit()
#
#
# @dp.message_handler()
# async def answer(message: types.Message):
#     blacK_user = cursor.execute('''SELECT reason FROM black_users WHERE user_id = ?''', \
#                                 (message.from_user.id,)).fetchone()
#     if blacK_user:
#         print(1)
#     else:
#         await message.answer(f'О, ты норм юзер, вот твой текст {message.text}')
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
#
