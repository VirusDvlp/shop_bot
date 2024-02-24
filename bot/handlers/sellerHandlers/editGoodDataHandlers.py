from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext

import aiogram.filters as f

from config import db
from FSM import AskGoodDataFSM
from filters import TextFilter, StartsWithFilter, CheckSellerFilter, Or, CheckAdminFilter

import keyboards as kb




async def ask_what_edit(message: types.Message, state: FSMContext):
    await state.set_state(AskGoodDataFSM.actionState)
    await message.answer(
        'Выберите, какие данные хотите изменить?',
        reply_markup=kb.good_data_change_kb
    )


async def ask_category(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AskGoodDataFSM)
    await state.update_data(action=callback.data.split('_')[1])
    await callback.message.answer('Выберите категорию, товар из которой хотите изменить', reply_markup=kb.get_choose_cat_kb())
    await callback.message.answer()


async def ask_good(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AskGoodDataFSM.goodState)
    category = callback.data.split('_')[1]
    await state.update_data(cat=category)
    await callback.message.answer(
        'Выберите товар для изменения данных',
        reply_markup=kb.get_choose_good_kb(category)
    )
    await callback.answer()



async def ask_data(callback: types.CallbackQuery, state: FSMContext):
    good = callback.data.split('_')[1]
    await state.set_state(AskGoodDataFSM.dataState)
    await state.update_data(
        good=good
    )
    await callback.message.answer(
        f'Введите новое значение'
    )
    await callback.answer()


async def edit_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data['action']
    good = data['good']
    value = message.text
    if action == 'price' or action == 'available':
        try:
            value = int(value)
            if value < 0:
                raise TypeError
        except TypeError:
            await message.answer('Значение должно быть числом большим либо равным нулю')
    db.edit_good_data(action, value, good)
    await state.clear()
    await message.answer('Значение успешно изменено')



def register_edit_good_data_handlers(dp: Dispatcher) -> None:
    dp.message.register(ask_what_edit, TextFilter('Изменить данные о товаре'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.callback_query.register(ask_category, StartsWithFilter('action_'), f.StateFilter(AskGoodDataFSM.actionState))
    dp.callback_query.register(ask_good, StartsWithFilter('cat_'), f.StateFilter(AskGoodDataFSM.catState))
    dp.callback_query.register(ask_data, StartsWithFilter('good_'), f.StateFilter(AskGoodDataFSM.goodState))
    dp.message.register(edit_data, f.StateFilter(AskGoodDataFSM.dataState))
