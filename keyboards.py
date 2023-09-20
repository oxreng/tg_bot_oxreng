from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btn_1 = KeyboardButton('Привет!')
btn_2 = KeyboardButton('Пока!')
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(btn_1, btn_2)

inline_btn_1 = InlineKeyboardButton('Первая кнопка', callback_data='button_1')
inline_kb = InlineKeyboardMarkup()
inline_kb.add(inline_btn_1)


# kb.add(button_1)
