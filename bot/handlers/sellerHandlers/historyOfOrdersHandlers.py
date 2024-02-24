from aiogram import types, Dispatcher

from filters import StartsWithFilter, TextFilter, CheckSellerFilter, Or, CheckAdminFilter
from config import db
from utils import get_basket_text
import keyboards as kb



async def ask_order_type(message: types.Message):
    await message.answer('Выберите, какие заказы хотите посмотреть', reply_markup=kb.orders_type_kb)


async def show_orders_by_category(callback: types.CallbackQuery):
    status = int(callback.data.split('_')[1])
    orders = db.get_orders_by_status(status)
    await callback.message.edit_reply_markup(
        reply_markup=kb.get_list_of_orders_kb(orders[0 : 5], 0, status)
    )
    await callback.answer()


async def next_page(callback: types.CallbackQuery):
    data = callback.data.split('_')
    page = int(data[1])
    orders = db.get_orders_by_status(data[2])
    page += 1
    if page + 1 * 5  - len(orders) > 5:
        await callback.answer('Выбрать страницу больше нельзя')
        return None
    await callback.message.edit_reply_markup(
        reply_markup=kb.get_list_of_orders_kb(orders[page * 5 : (page + 1) * 5], page, data[2])
    )


async def prev_page(callback: types.CallbackQuery):
    data = callback.data.split('_')
    page = int(data[1])
    orders = db.get_orders_by_status(data[2])
    if page == 0:
        await callback.answer('Выбрать страницу меньше нельзя')
        return None
    page -= 1
    await callback.message.edit_reply_markup(
        reply_markup=kb.get_list_of_orders_kb(orders[page * 5 : (page + 1) * 5], page, data[2])
    )


async def back_to_types(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите, какие заказы хотите посмотреть')
    await callback.message.edit_reply_markup(reply_markup=kb.orders_type_kb)
    await callback.answer()


async def show_data(callback: types.CallbackQuery):
    o_status = {
        0: 'ожидает подтверждения продавца',
        1: 'на стадии оформления',
        2: 'активный',
        3: 'завершился',
        4: 'отменён'
    }
    data = callback.data.split('_')
    order_data = db.get_order_data(data[1])
    text = get_basket_text(order_data['basket'].split(','), order_data['get_type'], order_data['text'])
    await callback.message.edit_text(
        text=f'''
Заказ - {order_data["date"]}
От пользователя - {order_data["name"]}, @{order_data["username"]}

Статус: {o_status[order_data["status"]]}

{text}
'''
    )
    keyboard = []
    if order_data["status"] == 0:
        keyboard.extend(kb.get_accept_order_req_kb(data[1]))
    elif order_data['status'] == 2:
        keyboard.extend(kb.get_ordering_kb(data[1]))
    keyboard.append([types.InlineKeyboardButton(text='Назад к списку заказов', callback_data=f'hprev_{int(data[1]) + 2}_{order_data["status"]}')])
    await callback.message.edit_reply_markup(
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    )
    await callback.answer()


def register_history_of_users_handlers(dp: Dispatcher) -> None:
    dp.message.register(ask_order_type, TextFilter('История заказов'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.callback_query.register(show_orders_by_category, StartsWithFilter('otype_'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.callback_query.register(next_page, StartsWithFilter('hnext_'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.callback_query.register(prev_page, StartsWithFilter('hprev_'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.callback_query.register(back_to_types, TextFilter('categories'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.callback_query.register(show_data, StartsWithFilter('horder_'), Or(CheckSellerFilter(), CheckAdminFilter()))
