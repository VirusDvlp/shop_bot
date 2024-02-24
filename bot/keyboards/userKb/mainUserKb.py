from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



main_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Каталог')],
        [KeyboardButton(text='Искать товары')],
        [KeyboardButton(text='Корзина')],
        [KeyboardButton(text='История заказов')],
        [KeyboardButton(text='О нас')]
    ],
    resize_keyboard=True
)
