from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def get_buy_order_kb(order_id) -> list:
    return [[InlineKeyboardButton(text='Оформление заказа', callback_data=f'buy_{order_id}')]]




ask_getting_type_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='ДОСТАВКОЙ НА ДОМ', callback_data=f'gt_home')],
        [InlineKeyboardButton(text='ЗАБРАТЬ В МАГАЗИНЕ', callback_data=f'gt_shop')]
    ]
)


choose_pay_type_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='ОНЛАЙН', callback_data='pt_0')],
        [InlineKeyboardButton(text='ОФФЛАЙН', callback_data='pt_1')]
    ]
)


choose_pay_sys_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Банковская карта', callback_data='ps_card')]
    ]
)


orders_type_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ожидающие подтверждения продавца', callback_data='otype_0')],
        [InlineKeyboardButton(text='Ожидающие оформления покупателем', callback_data='otype_1')],
        [InlineKeyboardButton(text='Действующие', callback_data='otype_2')],
        [InlineKeyboardButton(text='Завершенные', callback_data='otype_3')],
        [InlineKeyboardButton(text='Отменённые', callback_data='otype_4')]
    ]
)
