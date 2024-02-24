from aiogram.fsm.state import StatesGroup, State


class SearchInCatalogFSM(StatesGroup):
    textState = State()
