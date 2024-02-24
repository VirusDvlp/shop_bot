from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from filters import StartsWithFilter, TextFilter
from config import db
from FSM import SearchInCatalogFSM

import keyboards as kb



async def ask_search_word(m: types.Message, state: FSMContext):
    await state.set_state(SearchInCatalogFSM.textState)
    await m.answer('Введите текст, по которому будет производится поиск')


async def show_by_search(m: types.Message, state: FSMContext):
    await state.clear()
    goods = db.get_goods_by_search(m.text)
    if not goods:
        await m.answer('По данному запросу ничего не найдено')
        return None
    for good in goods:
        text = f"{good['name']}\n\n{good['descr']}\n\nЦена - {good['price']} руб\nВ наличи: {good['available']} шт."
        if good['image']:
            await m.answer_photo(
                photo=good['image'],
                caption=text,
                reply_markup=kb.get_add_to_basket_kb(good['id'])
            )
        else:
            await m.answer(
                text=text,
                reply_markup=kb.get_add_to_basket_kb(good['id'])
            )

async def ask_category(message: types.Message):
    await message.answer(
        'Выберите категорию товаров',
        reply_markup=kb.get_choose_cat_kb()
    )



async def show_goods_of_cat(callback: types.CallbackQuery):
    cat = callback.data.split('_')[1]
    goods = db.get_list_of_goods(cat)
    for good in goods:
        text = f"{good['name']}\n\n{good['descr']}\n\nЦена - {good['price']} руб\nВ наличи: {good['available']} шт."
        if good['image']:
            await callback.message.answer_photo(
                photo=good['image'],
                caption=text,
                reply_markup=kb.get_add_to_basket_kb(good['id'])
            )
        else:
            await callback.message.answer(
                text=text,
                reply_markup=kb.get_add_to_basket_kb(good['id'])
            )
    await callback.answer()


async def add_to_basket(callback: types.CallbackQuery):
    good = callback.data.split('_')[1]
    basket = db.get_user_basket(callback.from_user.id)
    basket.append(good)
    db.set_user_basket(callback.from_user.id, ','.join(basket))
    await callback.answer('Товар успешно добавлен в корзину')


def register_show_catalog_kb(dp: Dispatcher) -> None:
    dp.message.register(ask_category, TextFilter('Каталог'))
    dp.callback_query.register(show_goods_of_cat, StartsWithFilter('cat_'))
    dp.callback_query.register(add_to_basket, StartsWithFilter('good_'))

    dp.message.register(ask_search_word, TextFilter('Искать товары'))
    dp.message.register(show_by_search, StateFilter(SearchInCatalogFSM.textState))
