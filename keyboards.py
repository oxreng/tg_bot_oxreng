from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btn_1 = KeyboardButton('Привет!')
btn_2 = KeyboardButton('Пока!')
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(btn_1, btn_2)

kb_hw = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/add_bl')).add(KeyboardButton('/del_bl'))

inline_btn_0 = InlineKeyboardButton('Первая кнопка', callback_data='button_0')
inline_kb = InlineKeyboardMarkup()
inline_kb.add(inline_btn_0)

inline_btn_1 = InlineKeyboardButton('Первая кнопка', callback_data='btn_1')
inline_btn_2 = InlineKeyboardButton('Вторая кнопка', callback_data='btn_2')
inline_btn_3 = InlineKeyboardButton('Третья кнопка', callback_data='btn_3')
inline_btn_4 = InlineKeyboardButton('Четвёртая кнопка', callback_data='btn_4')
inline_btn_5 = InlineKeyboardButton('Пятая кнопка', callback_data='btn_5')
inline_kb_full = InlineKeyboardMarkup(row_width=2)

inline_kb_full.add(inline_btn_1, inline_btn_2)
inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)

inline_kb_full.insert(InlineKeyboardButton('query', switch_inline_query=''))
inline_kb_full.insert(InlineKeyboardButton('Yandex', url='https://www.yandex.ru'))








# kb.add(button_1)
