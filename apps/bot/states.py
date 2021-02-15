from aiogram.dispatcher.filters.state import StatesGroup, State


class BotForm(StatesGroup):
    main_menu = State()
    people_quantity = State()
    book_date = State()
    book_time = State()
    feedback_write = State()