from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db



def get_choose_cat_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    [builder.button(text=cat['name'], callback_data=f"cat_{cat['id']}") for cat in db.get_list_of_categories()]
    builder.adjust(1)
    return builder.as_markup()
