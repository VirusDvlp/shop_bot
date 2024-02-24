from aiogram.fsm.state import State, StatesGroup



class AddCategoryFSM(StatesGroup):
    nameState = State()
