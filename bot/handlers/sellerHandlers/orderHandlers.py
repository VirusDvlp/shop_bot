from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from filters import StartsWithFilter, CheckSellerFilter
from config import db
from FSM import CancelRequestFSM
import keyboards as kb


async def accept_order_req(callback: types.CallbackQuery):
    order_id = int(callback.data.split('_')[1])
    user_id = int(db.get_order_data(order_id)['user_id'])
    db.set_order_status(order_id, 1)
    try:
        await callback.bot.send_message(
            user_id,
            'Заявка на ваш заказ успешно принята продавцом, вы можете переходить к оформлению:',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb.get_buy_order_kb(order_id))
        )
    except Exception:
        pass
    await callback.answer('Заявка успешно одобрена')


async def cancel_order_req(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CancelRequestFSM.messageState)
    await state.update_data(order_id=int(callback.data.split('_')[1]))
    await callback.message.answer('Пришлите сообщение с причиной отказа, оно будет перешлено пользователю')
    await callback.answer()


async def get_cacnel_message(message: types.Message, state: FSMContext):
    s_data = await state.get_data()
    await state.clear()
    order_id = s_data['order_id']
    user_id = int(db.get_order_data(order_id)['user_id'])
    db.set_order_status(order_id, 4)
    try:
        await message.bot.send_message(
            user_id,
            f'Заявка на ваш заказ отклонена продавцом. Сообщение от продавца:\n{message.text}'
        )
    except Exception:
        pass
    await message.answer('Заявка успешно отклонена')


async def get_succesfull_order(callback: types.CallbackQuery):
    order = int(callback.data.split('_')[1])
    db.set_order_status(order, 4)
    await callback.answer()


async def cancel_order(c: types.CallbackQuery, state: FSMContext):
    order = int(c.data.split('_')[1])
    await state.set_state(CancelRequestFSM.messageOrderState)
    await state.update_data(order=order)
    await c.message.answer(
        'Введите сообщение, которое будет показано пользователю'
    )
    await c.answer()


async def get_cancel_order_message(m: types.Message, state: FSMContext):
    order = await state.get_data().cr_await['order']
    await state.clear()
    o_data = db.get_order_data(order)
    db.set_order_status(order, 4)
    try:
        await m.bot.send_message(int(o_data), f'Ваш заказ отменен, сообщение от продавца:\n{m.text}')
    except Exception:
        pass
    await m.answer('Заказ успешно отменен!')


def register_order_handlers(dp: Dispatcher) -> None:
    dp.callback_query.register(accept_order_req, StartsWithFilter('accoreq_'), CheckSellerFilter())
    dp.callback_query.register(cancel_order_req, StartsWithFilter('canclreq_'), CheckSellerFilter())
    dp.message.register(get_cacnel_message, StateFilter(CancelRequestFSM.messageState), CheckSellerFilter())
    dp.callback_query.register(get_succesfull_order, StartsWithFilter('finish_'), CheckSellerFilter())
    dp.callback_query.register(cancel_order, StartsWithFilter('ocancel_'), CheckSellerFilter())
    dp.message.register(get_cancel_order_message, StateFilter(CancelRequestFSM.messageOrderState))
