from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db


def get_list_of_orders_kb(orders: list, page, status) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.button(text=f"{order['date'].date()} - {order['username']}", callback_data=f'horder_{order["id"]}_{page}')
    builder.adjust(1)
    builder.row(
        InlineKeyboardButton(text='<-', callback_data=f'hprev_{page}_{status}'),
        InlineKeyboardButton(text='->', callback_data=f'hnext_{page}_{status}')
    )
    builder.row(InlineKeyboardButton(text='К списку категорий', callback_data=f'categories'))
    return builder.as_markup()
