from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_accept_order_req_kb(order_id) -> list:
    return [
        [InlineKeyboardButton(text='Одобрить заявку', callback_data=f'accoreq_{order_id}')],
        [InlineKeyboardButton(text='Отклонить заявку', callback_data=f'canclreq_{order_id}')]
    ]

def get_ordering_kb(order_id) -> list:
    return [
        [InlineKeyboardButton(text='Покупатель получил заказ', callback_data=f'finish_{order_id}')],
        [InlineKeyboardButton(text='Отменить заказ', callback_data=f'ocancel_{order_id}')]
    ]
