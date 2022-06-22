from aiogram.dispatcher.filters.state import StatesGroup, State

class UserAddStates(StatesGroup):
    waiting_for_brand_name = State()
    waiting_for_seller_name = State()
    waiting_for_confirm = State()

    