from aiogram import types, Dispatcher

from config import db
from filters import TextFilter, StartsWithFilter
from utils import count_basket_total

import keyboards as kb


async def send_basket(message: types.Message):
    basket = db.get_user_basket(message.from_user.id)
    if '' in basket:
        basket.remove('')
    total = count_basket_total(basket)
    await message.answer(
        text=f'Корзина\n\nКол-во товаров: {len(basket)}\nИТОГО:{total}',
        reply_markup=kb.get_basket_kb(basket, 0)
    )


async def prev_page(callback: types.CallbackQuery):
    page = int(callback.data.split('_')[1])
    if page <= 0:
        await callback.answer('Выбрать страницу меньше нельзя')
    else:
        basket = db.get_user_basket(callback.from_user.id)
        if '' in basket:
            basket.remove('')
        total = count_basket_total(basket)
        page -= 1
        await callback.message.edit_text(text=f'Корзина\n\nКол-во товаров: {len(basket)}\nИТОГО:{total}')
        await callback.message.edit_reply_markup(reply_markup=kb.get_basket_kb(basket, page))
    await callback.answer()


async def next_page(callback: types.CallbackQuery):
    page = int(callback.data.split('_')[1])
    basket = db.get_user_basket(callback.from_user.id)
    if '' in basket:
        basket.remove('')
    total = count_basket_total(basket)
    page += 1
    await callback.message.edit_text(text=f'Корзина\n\nКол-во товаров: {len(basket)}\nИТОГО:{total}')
    await callback.message.edit_reply_markup(reply_markup=kb.get_basket_kb(basket, page))
    await callback.answer()


async def plus_good(callback: types.CallbackQuery):
    data = callback.data.split('_')
    good = data[1]
    page = int(data[2])
    basket = db.get_user_basket(callback.from_user.id)
    basket.append(good)
    db.set_user_basket(callback.from_user.id, ','.join(basket))
    if '' in basket:
        basket.remove('')
    total = count_basket_total(basket)
    await callback.message.edit_text(text=f'Корзина\n\nКол-во товаров: {len(basket)}\nИТОГО:{total}')
    await callback.message.edit_reply_markup(reply_markup=kb.get_basket_kb(basket, page))
    await callback.answer()


async def minus_good(callback: types.CallbackQuery):
    data = callback.data.split('_')
    good = data[1]
    page = int(data[2])
    basket = db.get_user_basket(callback.from_user.id)
    try:
        basket.remove(good)
        db.set_user_basket(callback.from_user.id, ','.join(basket))
    except ValueError:
        return None
    total = count_basket_total(basket)
    await callback.message.edit_text(text=f'Корзина\n\nКол-во товаров: {len(basket)}\nИТОГО:{total}')
    await callback.message.edit_reply_markup(reply_markup=kb.get_basket_kb(basket, page))
    await callback.answer()


async def kill_good(callback: types.CallbackQuery):
    data = callback.data.split('_')
    good = data[1]
    page = int(data[2])
    basket = db.get_user_basket(callback.from_user.id)
    [basket.remove(good) for i in range(basket.count(good))]
    db.set_user_basket(callback.from_user.id, ','.join(basket))
    if '' in basket:
        basket.remove('')
    total = count_basket_total(basket)
    page += 1
    await callback.message.edit_text(text=f'Корзина\n\nКол-во товаров: {len(basket)}\nИТОГО:{total}')
    await callback.message.edit_reply_markup(reply_markup=kb.get_basket_kb(basket, page))
    await callback.answer()


def register_basket_handlers(dp: Dispatcher):
    dp.message.register(send_basket, TextFilter('Корзина'))
    dp.callback_query.register(prev_page, StartsWithFilter('prev_'))
    dp.callback_query.register(next_page, StartsWithFilter('next_'))
    dp.callback_query.register(plus_good, StartsWithFilter('plus_'))
    dp.callback_query.register(minus_good, StartsWithFilter('minus_'))
    dp.callback_query.register(kill_good, StartsWithFilter('kill_'))
