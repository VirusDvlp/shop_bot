from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



main_seller_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить данные товаров')
        ],
        [
            KeyboardButton(text='Добавить новый товар')
        ],
        [
            KeyboardButton(text='Добавить новую категорию товаров')
        ],
        [
            KeyboardButton(text='История заказов')
        ],
        [
            KeyboardButton(text='Сдать смену')
        ]
    ]
)

get_shift_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Взять смену')]
    ]
)
