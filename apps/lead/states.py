from aiogram.dispatcher.filters.state import StatesGroup, State


class CustomerForm(StatesGroup):
    language_choice = State()
    phone_number = State()
    full_name = State()


class LeadForm(StatesGroup):
    residence_choice = State()
    room_quantity_choice = State()
    apartment_choice = State()
    lead_request = State()
