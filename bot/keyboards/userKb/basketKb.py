from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db


def get_basket_kb(basket: list, page: int) -> InlineKeyboardMarkup:
    uniq_basket = set(basket)
    length = len(uniq_basket)
    goods = InlineKeyboardBuilder()
    if length == 0:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В корзине пусто', callback_data='empty')]])
    elif length > 5:
        uniq_basket = uniq_basket[page * 5 : (page + 1) * 5]
    for good in uniq_basket:
        good_data = db.get_good_data(good)
        goods.row(InlineKeyboardButton(text=f'{good_data["name"]} - {good_data["price"] * basket.count(good)}', callback_data=' '),)
        goods.row(
            InlineKeyboardButton(text='+', callback_data=f'plus_{good}_{page}'),
            InlineKeyboardButton(text=str(basket.count(good)), callback_data=' '),
            InlineKeyboardButton(text='-', callback_data=f'minus_{good}_{page}'),
            InlineKeyboardButton(text='/\\', callback_data=f'kill_{good}_{page}')
        )
    page += 1
    if length > 5:
        delta = length - page * 5
        if delta <= -5:
            goods.button(text='<-', callback_data=f'prev_{page}')
            goods.button(text=f'{page} из {basket / 5}')
        else:
            goods.button(text='->', callback_data=f'next_{page}')
    goods.row(InlineKeyboardButton(text='ОФОРМИТЬ ЗАКАЗ', callback_data='oreq'))
    return goods.as_markup()
