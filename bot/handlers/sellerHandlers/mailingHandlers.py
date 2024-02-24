from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from FSM import MailingFSM
from filters import TextFilter, Or, CheckSellerFilter, CheckAdminFilter
from config import db


async def ask_mailing_text(m: types.Message, state: FSMContext):
    await state.set_state(MailingFSM.textState)
    await m.answer('Введите текст сообщения с рассылкой')


async def ask_photo(m: types.Message, state: FSMContext):
    await state.set_state(MailingFSM.photoState)
    await state.update_data(text=m.text)
    await m.answer('Пришлите фото для сообщения с рассылкой, если его не должно быть, то пришлите любой текст')


async def mailing(m: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    users = db.get_users()
    if m.content_type == types.ContentType.PHOTO:
        for user in users:
            await m.bot.send_photo(
                user['user_id'],
                m.photo[-1].file_id,
                caption=data['text']
            )
    else:
        for user in users:
            await m.bot.send_message(
                user['user_id'],
                text=data['text']
            )
    await m.answer('Рассылка успешно отправлена')



def register_mailing_handlers(dp: Dispatcher) -> None:
    dp.message.register(ask_mailing_text, TextFilter('Новая рассылка'), Or(CheckSellerFilter(), CheckAdminFilter()))
    dp.message.register(ask_photo, StateFilter(MailingFSM.textState))
    dp.message.register(mailing, StateFilter(MailingFSM.photoState))
