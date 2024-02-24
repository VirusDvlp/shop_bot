from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
import aiogram.filters as f

from FSM import AddGoodFSM
from config import db
from filters import TextFilter, StartsWithFilter, CheckSellerFilter, Or, CheckAdminFilter
import keyboards as kb


async def ask_name(message: types.Message, state: FSMContext):
    await state.set_state(AddGoodFSM.nameState)
    await message.answer('Введите название товара')


async def ask_descr(message: types.Message, state: FSMContext):
    await state.set_state(AddGoodFSM.descrState)
    await state.update_data(name=message.text)
    await message.answer('Введите описание товара')


async def ask_price(message: types.Message, state: FSMContext):
    await state.set_state(AddGoodFSM.priceState)
    await state.update_data(descr=message.text)
    await message.answer('Введите цену товара')


async def ask_image(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
    except ValueError:
        await message.answer('Введите число!!!')
        return None
    await state.set_state(AddGoodFSM.imageState)
    await state.update_data(price=price)
    await message.answer('Пришлите изображение для товара, если их не должно быть, то пришлите любой текст')


async def ask_category(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
        await state.update_data(image=message.photo[-1].file_id)
    else:
        await state.update_data(image='')
    await state.set_state(AddGoodFSM.categoryState)
    await message.answer('Выберите, к какой катеории будет относится товар', reply_markup=kb.get_choose_cat_kb())


async def add_good(callback: types.CallbackQuery, state: FSMContext):
    print(123)
    cat = int(callback.data.split('_')[1])
    data = await state.get_data()
    await state.clear()
    db.add_good(
        data['name'],
        data['descr'],
        data['price'],
        cat,
        data['image']
    )
    try:
        await callback.message.delete()
    except Exception:
        await callback.message.edit_reply_markup(types.InlineKeyboardMarkup())
    await callback.message.answer('Товар успешно добавлен в каталог')
    await callback.answer()



def register_add_good_handlers(dp: Dispatcher) -> None:
    dp.message.register(ask_name, TextFilter('Добавить новый товар'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.message.register(ask_descr, f.StateFilter(AddGoodFSM.nameState))
    dp.message.register(ask_price, f.StateFilter(AddGoodFSM.descrState))
    dp.message.register(ask_image, f.StateFilter(AddGoodFSM.priceState))
    dp.message.register(ask_category, f.StateFilter(AddGoodFSM.imageState))
    dp.callback_query.register(add_good, StartsWithFilter('cat_'), f.StateFilter(AddGoodFSM.categoryState))
