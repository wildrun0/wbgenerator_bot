from aiogram.dispatcher.filters.state import StatesGroup, State

class ProductAddStates(StatesGroup):
    waiting_product_name = State()
    waiting_product_barcode = State()
    waiting_product_articul = State()

    waiting_product_additional = State()