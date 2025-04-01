from aiogram.dispatcher.filters.state import State, StatesGroup

class User(StatesGroup):
    enter_code = State()

    admin = State()
    enter_count = State()
    test = State()
    remove_user = State()
