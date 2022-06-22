from aiogram import types

menu_kb_btn = types.KeyboardButton(text="⏪Выйти в меню", callback_data="Menu")
create_stickers_kb_btn = types.KeyboardButton(text="➡️Создать наклейки", callback_data="CreateWBSticker")

home_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False, row_width=1
).add(
    create_stickers_kb_btn,
    types.KeyboardButton(text="ℹ️Моя информация", callback_data="MyWBInfo"),
    types.KeyboardButton(text="✏️Добавить товары", callback_data="AddWBProducts")
)

menu_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False, row_width=1
).add(menu_kb_btn)

yes_no_kb = types.ReplyKeyboardMarkup(row_width=1)
yes_no_kb.add(
    types.KeyboardButton(text="✅Да"),
    types.KeyboardButton(text="🚫Нет")
)

fill_brand_info_btn = types.InlineKeyboardMarkup()
fill_brand_info_btn.add(
    types.InlineKeyboardMarkup(text='✏️📗 Заполнить информацию о бренде', callback_data='ProductsADD')
)

fill_brand_done = types.InlineKeyboardMarkup(row_width=1)
fill_brand_done.add(
    types.InlineKeyboardButton(text="✅Все верно", callback_data="ChangeDone"),
    types.InlineKeyboardButton(text="✏️Изменить бренд", callback_data="ChangeBrand"),
    types.InlineKeyboardButton(text="✏️Изменить продавца", callback_data="ChangeSeller")
)

stickers_confirm_kb = types.ReplyKeyboardMarkup(row_width=1)
stickers_confirm_kb.add(
    types.KeyboardButton(text="⏭️Продолжить", callback_data="WBStickers_Done"),
    menu_kb_btn,
)

stickers_confirm_done = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False, row_width=1
).add(
    create_stickers_kb_btn,
    menu_kb_btn
)

product_add_done = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False, row_width=1
).add(
    types.KeyboardButton(text="✅Завершить", callback_data="ProductAddStop"),
    menu_kb_btn
)