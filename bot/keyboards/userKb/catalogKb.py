from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def get_add_to_basket_kb(good_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'good_{good_id}')]
        ]
    )


def get_select_good_number(good_id, number=1) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='+', callback_data=f'plcat_{good_id}_{number}'),
                InlineKeyboardButton(text=number, callback_data=f'a'),
                InlineKeyboardButton(text='-', callback_data=f'mcat_{good_id}_{number}')
            ]
        ]
    )



cats_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Категория 1', callback_data='cat_1')],
        [InlineKeyboardButton(text='Категория 2', callback_data='cat_2')],
        [InlineKeyboardButton(text='Категория 3', callback_data='cat_3')]
    ]
)
