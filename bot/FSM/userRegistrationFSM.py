from aiogram.fsm.state import State, StatesGroup


class UserRegistrationFSM(StatesGroup):
    nameState = State()
