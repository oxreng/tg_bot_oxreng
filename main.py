from config import Config
import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt

bot = Bot(token=Config.TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(text='1')
async def cmd_test_1(message: types.Message):
    await message.reply(f'Привет *{message.from_user.username}*')


@dp.message_handler(text='2')
async def cmd_text_2(message: types.Message):
    await message.answer(
        fmt.text(
            fmt.text(fmt.hunderline('Яблоки'), 'вес 1 кг\n'),
            fmt.text('Старая цена: ', fmt.hstrikethrough(50), 'рублей\n'),
            fmt.text('Новая цена: ', fmt.hbold(25), 'рублей')
        ), parse_mode=types.ParseMode.HTML
    )


@dp.message_handler(text='Три')
async def cmd_text_3(message: types.Message):
    await message.answer(message.text)
    await message.answer(message.md_text)
    await message.answer(message.html_text)
    await message.answer(f'<u>Ваш текст</u>:\n\n{message.html_text}', parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
