from aiogram.dispatcher.filters.state import StatesGroup, State


class CustomerForm(StatesGroup):
    language_choice = State()
    phone_number = State()
