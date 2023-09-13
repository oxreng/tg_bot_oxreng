from config import Config
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

cities = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Нижний Новгород",
    "Казань",
    "Челябинск",
    "Омск",
    "Самара",
    "Ростов-на-Дону",
]


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    '''Здоровается и показывает кнопку "Weather"'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton('Weather')
    keyboard.add(button)
    await message.answer('Привет, я бот с погодой нажми Weather, чтобы выбрать город!', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'weather')
async def cmd_weather(message: types.Message):
    """Отправляет пользователю список городов для выбора погоды"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [types.KeyboardButton(city) for city in cities]
    keyboard.add(*buttons)
    await message.answer('Выберите город, чтобы узнать погоду', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in cities)
async def get_weather(message: types.Message):
    """Получает погоду для выбранного города и отправляет юзеру"""
    city = message.text
    api_key = Config.KEY
    weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'

    try:
        r = requests.get(weather_api_url)
        data = r.json()

        if r.status_code == 200:
            temperature = data['main']['temp']
            weather_desc = data['weather'][0]['description']
            speed_wind = data['wind']['speed']

            await message.answer(f'Погода в городе {city}:\nТемпепатура: {temperature}°C\n'
                                 f'Описание: {weather_desc}\nСкорость ветра: {speed_wind} м/с')

        else:
            await message.answer('Не удалось получить данные :(')
    except Exception as e:
        await message.answer('Произошла ошибка при получении данных')
        logging.error(e)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
