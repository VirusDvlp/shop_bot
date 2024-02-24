from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_admin_kb = ReplyKeyboardMarkup(
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
        ]
    ]
)
