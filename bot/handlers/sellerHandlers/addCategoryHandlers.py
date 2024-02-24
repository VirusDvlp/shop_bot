from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from filters import TextFilter, CheckSellerFilter, Or, CheckAdminFilter
from config import db
from FSM import AddCategoryFSM


async def ask_name(message: types.Message, state: FSMContext):
    await state.set_state(AddCategoryFSM.nameState)
    await message.answer('Введите название категории')


async def add_category(message: types.Message, state: FSMContext):
    await state.clear()
    db.add_category(message.text)
    await message.answer('Категория успешно добавлена')


def register_add_category(dp: Dispatcher) -> None:
    dp.message.register(ask_name, TextFilter('Добавить новую категорию товаров'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.message.register(add_category, StateFilter(AddCategoryFSM.nameState))
