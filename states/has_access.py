from aiogram.dispatcher.filters.state import StatesGroup, State

class UserSteps(StatesGroup):
    init_state = State()
    main_state = State()