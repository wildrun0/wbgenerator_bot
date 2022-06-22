from aiogram.dispatcher.filters.state import StatesGroup, State

class StickerCreateStates(StatesGroup):
    waiting_for_product = State()
    waiting_for_confirm = State()
    waiting_for_screens = State()
    