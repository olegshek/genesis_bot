from aiogram.dispatcher.filters.state import StatesGroup, State


class InformationForm(StatesGroup):
    information_state = State()
