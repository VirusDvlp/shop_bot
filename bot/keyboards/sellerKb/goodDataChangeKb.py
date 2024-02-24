from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppData, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db


def get_choose_good_kb(cat) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    goods = db.get_list_of_goods(cat)
    [builder.button(text=good['name'], callback_data=f"good_{good['id']}") for good in goods]
    builder.adjust(1)
    return builder.as_markup()



good_data_change_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Данные о наличии товара', callback_data='action_available')],
        [InlineKeyboardButton(text='Данные о цене', callback_data='action_price')],
        [InlineKeyboardButton(text='Данные об описании товара', callback_data='action_descr')]
    ]
)
