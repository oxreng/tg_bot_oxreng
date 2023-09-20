from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but_start_1 = KeyboardButton('Напитки')
but_start_2 = KeyboardButton('Закуски')
but_back = KeyboardButton('Назад')
but_zak_1 = KeyboardButton('Начос')
but_zak_2 = KeyboardButton('Чипсы')
but_zak_3 = KeyboardButton('Сухарики')
but_drink_1 = KeyboardButton('Сок')
but_drink_2 = KeyboardButton('Вода')
but_drink_3 = KeyboardButton('Газировка')

# add - только 1 кнопку, row - несколько сразу не переносит на др строку, insert - тот же row, н с переносом
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add(but_start_1, but_start_2)
kb_zak = ReplyKeyboardMarkup(resize_keyboard=True)
kb_zak.add(but_zak_1, but_zak_2, but_zak_3, but_back)
kb_drink = ReplyKeyboardMarkup(resize_keyboard=True)
kb_drink.add(but_drink_1, but_drink_2, but_drink_3, but_back)

# kb.add(button_1)
