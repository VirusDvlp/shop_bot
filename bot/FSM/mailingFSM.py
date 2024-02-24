from aiogram.fsm.state import State, StatesGroup


class MailingFSM(StatesGroup):
    textState = State()
    photoState = State()
