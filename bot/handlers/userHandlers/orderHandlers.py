from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
import aiogram.filters as f

from aiofiles import open as o

from json import loads

from config import db
from filters import TextFilter, StartsWithFilter
from FSM import OrderRequestFSM, OrderBuyFSM
from utils import get_basket_text, count_basket_total
import keyboards as kb


async def ask_getting_type(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderRequestFSM.gettingTypeState)
    await callback.message.answer('Выберите, как хотите получить заказ', reply_markup=kb.ask_getting_type_kb)
    await callback.answer()


async def ask_adress(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderRequestFSM.whereState)
    await callback.message.answer(
        'Пришлите геопозицию, куда нужно доставить заказ'
    )
    await callback.answer()



async def get_adress(message: types.Message, state: FSMContext):
    location = message.location
    await get_request(message, message.from_user.id, location.latitude, location.longitude, 1)


async def get_in_shop(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await get_request(callback.message, callback.from_user.id, 0, 0, 0)


async def get_request(message: types.Message, user_id, lat, lon, get_type):
    user_id = user_id
    basket = db.get_user_basket(user_id)
    total = count_basket_total(basket)
    db.clear_user_basket(user_id)
    id = db.add_order_request(user_id, ','.join(basket), lat, lon, get_type, get_type, total)
    async with o('sellers_data.json') as file:
        data = loads(await file.read())
    if data['cur_seller'] != 0:
        await message.bot.send_message(
            data['cur_seller'],
            text=f'Поступила заявка на заказ.\n\n{get_basket_text(basket, get_type, total)}',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb.get_accept_order_req_kb(id))
        )
        if get_type == 1:
            await message.bot.send_location(
                data['cur_seller'],
                lat,
                lon
            )
    await message.answer(
        'Ваша заявка на заказ отправлена продавцу, как только он её одобрит, вы сможете перейти к оформлению'
        )
    


async def ask_pay_sys(callback: types.CallbackQuery, state: FSMContext):
    order = int(callback.data.split('_')[1])
    o_data = db.get_order_data(order)
    if o_data['get_type'] == 1:
        await state.set_state(OrderBuyFSM.paySysState)
        await state.update_data(order=order)
        await callback.message.answer(
            'Выберите платежную систему, через которую хотите оплатить',
            reply_markup=kb.choose_pay_type_kb
        )
    else:
        await state.clear()
        db.set_order_status(order, 2)
        async with o('sellers_data.json', 'r') as file:
            data = loads(await file.read())
        if data['cur_seller'] != 0:
            total = count_basket_total(o_data['basket'])
            text = get_basket_text(o_data['basket'].split(','), o_data['get_type'], total)
            await callback.bot.send_message(
                data['cur_seller'],
                f'''
Поступил заказ от пользователя - {o_data["name"]}, @{o_data["username"]}
{text}
''',
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb.get_ordering_kb(order))
            )
            if o_data['get_type'] == 1:
                await callback.bot.send_location(
                    o_data['cur_seller'],
                    latitude=o_data['lat'],
                    longitude=o_data['lon']
                )
        await callback.message.answer('Заказ успешно оформлен')
    await callback.answer()


async def pay(callback: types.CallbackQuery, state: FSMContext):
    order = state.get_data()["order"]
    await state.clear()
    order_data = db.get_order_data(order)
    total = order_data['total']
    await callback.message.answer_invoice(
        title='Оплата заказа',
        description='Оплата заказа',
        payload=f'order_{order}',
        currency='rub',
        prices=[
            types.LabeledPrice(label='Корзина', amount=total*100),
            types.LabeledPrice('Доставка', amount=10000)
        ]
    )
    await callback.answer()


async def precheckout_query(precheckout: types.PreCheckoutQuery):
    order = int(precheckout.invoice_payload.split('_')[1])
    answer = False
    order_d = db.get_order_data(order)
    if order_d:
        if order_d['status'] == 2:
            answer = True
    await precheckout.answer(answer)


async def succesfull_payment(message: types.Message):
    order_id = int(message.successful_payment.invoice_payload.split('_')[1])
    order = db.get_order_data(order_id)
    db.set_order_status(order_id, 2)
    async with o('sellers_data.json', 'r') as file:
        data = loads(await file.read())
    if data['cur_seller'] != 0:
        text = get_basket_text(order['basket'].split(','), order['get_type'], order['total'])
        await message.bot.send_message(
            data['cur_seller'],
            f'''
Поступил заказ от пользователя - {order["name"]}, @{order["username"]}
{text}
''',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb.get_ordering_kb(order_id))
        )
        if order['get_type'] == 1:
            await message.bot.send_location(
                order['cur_seller'],
                latitude=order['lat'],
                longitude=order['lon']
            )
    await message.answer('Ваша заказ отправлен в магазин')


async def cancel_order(callback: types.CallbackQuery):
    order_id = callback.data.split('_')[1]
    db.set_order_status(order_id, 3)
    async with o('sellers_data.json', 'r') as file:
        data = loads(file)
    if data['cur_seller'] != 0:
        user = db.get_user_data(callback.from_user.id)
        try:
            await callback.bot.send_message(
                data['cur_seller'],
                f'Пользователь {user["name"]}, @{user["username"]}, отказался от заказа'
            )
        except Exception:
            pass
    await callback.message.answer('Заказ успешно отменен')
    await callback.answer()


async def finish_order(callback: types.CallbackQuery):
    order_id = callback.data.split('_')[1]
    db.set_order_status(order_id, 3)
    async with o('sellers_data.json', 'r') as file:
        data = loads(file)
    if data['cur_seller'] != 0:
        user = db.get_user_data(callback.from_user.id)
        try:
            await callback.bot.send_message(
                data['cur_seller'],
                f'Пользователь {user["name"]}, @{user["username"]}, указал, что получил заказ'
            )
        except Exception:
            pass
    await callback.messa
    await callback.message.answer('Заказ успешно завершен')
    await callback.answer()


def register_order_req_handlers(dp: Dispatcher):
    dp.callback_query.register(ask_getting_type, TextFilter('oreq'))
    dp.callback_query.register(ask_adress, StartsWithFilter('gt_home'), f.StateFilter(OrderRequestFSM.gettingTypeState))
    dp.message.register(get_adress, lambda mess: mess.content_type == types.ContentType.LOCATION, f.StateFilter(OrderRequestFSM.whereState))
    dp.callback_query.register(get_in_shop, TextFilter('gt_shop'), f.StateFilter(OrderRequestFSM.gettingTypeState))

    dp.callback_query.register(ask_pay_sys, StartsWithFilter('buy_'))
    dp.callback_query.register(pay, StartsWithFilter('ps_'), f.StateFilter(OrderBuyFSM.paySysState))
    dp.pre_checkout_query.register(precheckout_query)
    dp.message.register(succesfull_payment, lambda mess: mess.content_type == types.ContentType.SUCCESSFUL_PAYMENT)

    dp.callback_query.register(cancel_order, StartsWithFilter('ocancel_'))
    dp.callback_query.register(finish_order, StartsWithFilter('finish_'))
