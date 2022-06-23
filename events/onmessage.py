import logging
import traceback
from io import BytesIO
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import UserAddStates, ProductAddStates, StickerCreateStates

from keyboardx import *
from loader import dp
from loader import userhandler as uh
from loader import bargenerator as bargen
from loader import stickerlabelgenerator as stickerlabel

@dp.message_handler(commands="start")
async def on_start(message: types.Message):
    uid = message.from_user.id
    uh.create_user(uid)

    await message.answer((
        "👋 Привет. Я помогу тебе упростить жизнь с заказами на WB\n"
        "Для начала, заполни информацию о своем бренде👇"
    ), reply_markup=fill_brand_info_btn) 

@dp.callback_query_handler(text="ProductsADD")
async def add_brand(callback : types.CallbackQuery):
    await callback.message.answer((
        "Давай теперь заполним информацию о бренде! :)\n"
        "Введи название:"
    ))
    await UserAddStates.waiting_for_brand_name.set()

@dp.message_handler(state=UserAddStates.waiting_for_brand_name)
async def brand_setted(message: types.Message, state: FSMContext):
    await state.update_data(brand=message.text)
    brand_data = await state.get_data()
    if "seller" in brand_data:
        await message.answer((
            f"• Бренд: <b>{brand_data['brand']}</b>\n"
            f"• Продавец: <b>{brand_data['seller']}</b>\n"
            "Всё верно?"
        ), reply_markup=fill_brand_done)
        await UserAddStates.waiting_for_confirm.set()
    else:
        await message.answer((
            f"• Бренд: <b>{message.text}</b>\n"
            "• Продавец: ?\n"
            "Введи продавца:"
        ))
        await UserAddStates.next()

@dp.message_handler(state=UserAddStates.waiting_for_seller_name)
async def brand_setted(message: types.Message, state: FSMContext):
    await state.update_data(seller=message.text)
    brand_data = await state.get_data()
    await message.answer((
        f"• Бренд: <b>{brand_data['brand']}</b>\n"
        f"• Продавец: <b>{brand_data['seller']}</b>\n"
        "Всё верно?"
    ), reply_markup=fill_brand_done)
    await UserAddStates.next()

@dp.callback_query_handler(state=UserAddStates.waiting_for_confirm, text="ChangeBrand")
async def setting_done(callback : types.CallbackQuery):
    await UserAddStates.waiting_for_brand_name.set()
    await callback.message.answer("Введите новое название бренда:")

@dp.callback_query_handler(state=UserAddStates.waiting_for_confirm, text="ChangeSeller")
async def setting_done(callback : types.CallbackQuery):
    await UserAddStates.waiting_for_seller_name.set()
    await callback.message.answer("Введите нового продавца:")
    
@dp.message_handler(state="*", text="⏪Выйти в меню")
async def wb_home(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        if "ProductAddStates" in current_state:
            product = await state.get_data()
            try:
                uh.product_del(message.from_user.id, product["articul"])
            except: pass
        await state.finish()
    await message.answer((
        "Главное меню бота"
    ), reply_markup = home_keyboard)
    
@dp.callback_query_handler(state=UserAddStates.waiting_for_confirm, text="ChangeDone")
async def setting_done(callback : types.CallbackQuery, state: FSMContext):
    brand_data = await state.get_data()
    uid = callback.from_user.id
    await callback.message.answer((
        "Поздравляю! Вы заполнили информацию о продавце. Сохраняю данные..⏲️\n"
        "Теперь можно приступить к заполнению вашего ассортимена!"
    ), reply_markup = home_keyboard)

    uh.add_dict(uid, brand_data)
    await state.finish()

@dp.message_handler(text = "➡️Создать наклейки")
async def wb_createSticker(message : types.Message):
    uid = message.from_user.id
    wb_products = uh.get_products(uid)
    if len(wb_products) == 0:
        await message.answer((
        "⛔У вас нет добавленных товаров!\n"
        "Сначала добавьте товары, потом можно будет создать этикетки"))
    else:
        await message.answer("Загружаю данные ...", reply_markup=menu_keyboard)
        prods = []
        for i in wb_products:
            prods.append(types.InlineKeyboardButton(text=f"({i}){uh.get_product(uid, i)['Наименование']}", callback_data=f"WBSticker_create:{i}"))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*prods)
        
        await message.answer("Выберите товар(артикул), для которого создаем этикетку:", reply_markup=keyboard)
        await StickerCreateStates.waiting_for_product.set()

@dp.callback_query_handler(state=StickerCreateStates.waiting_for_product)
async def wb_sticker_product(callback: types.CallbackQuery, state: FSMContext):
    product = callback.data.replace("WBSticker_create:","")
    product_name = uh.get_product(callback.from_user.id, product)['Наименование']
    await state.update_data(articul = product)
    await state.update_data(name = product_name)
    await StickerCreateStates.next()
    
    await callback.message.answer((
        f"Выбран товар: <b>{product_name}</b>\n"
        "Нужно продублировать в документе маркировки товара (без штрихкодов клиентов)?"
    ), reply_markup=yes_no_kb)

@dp.message_handler(text=["✅Да", "🚫Нет"], state=StickerCreateStates.waiting_for_confirm)
async def wb_sticker_additional(message: types.Message, state: FSMContext):
    product_name = await state.get_data()
    await state.update_data(double=(True if message.text == "✅Да" else False))
    await state.update_data(photos=[])
    await StickerCreateStates.next()

    await message.answer((
        f"Выбран товар: <b>{product_name['name']}</b>\n"
        f"Дублирование маркировок товара: <b>{message.text}</b>\n"
        "Отправьте боту скачанные этикетки с клиентами:\n"
        "<u>Важно!</u> Используйте этикетки <u><b>50х40</b></u>. Размеры меньше получатся мелковатыми\n"
        "После того как загрузите, нажмите на кнопку 'Продолжить'"
    ), reply_markup=stickers_confirm_kb)
    
@dp.message_handler(content_types=['photo'], state=StickerCreateStates.waiting_for_screens)
async def wb_sticker_screens(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photos"] = [*data["photos"], message.photo[-1]]

@dp.message_handler(text="⏭️Продолжить", state=StickerCreateStates.waiting_for_screens)
async def wb_sticker_done(message : types.Message, state: FSMContext):
    product = await state.get_data()
    if len(product["photos"]) > 0:
        uid = message.from_user.id
        await message.answer("Генерирую изображения, подождите...")

        for photo in product["photos"]:
            byte_photo = BytesIO()
            await photo.download(
                destination_file = byte_photo
            )
            stickerlabel.sticker_add(uid, byte_photo, product['double'])
        try:
            docx = types.InputFile(stickerlabel.complete_file(uid, product["articul"]))
            await message.answer(
                f"🎉Готово! По вашему запросу сгенерировано <u>{len(product['photos'])}</u> этикеток(-а)"
            )
            await state.finish()
            await message.answer_document(docx, reply_markup=stickers_confirm_done)
            stickerlabel.clear(uid, temp_files=True)
        except Exception as e:
            await state.update_data(counter=0)
            await state.update_data(photos=[])
            await message.answer((
                "Произошла ошибка при создании этикеток!\n"
                f"Ошибка: <b>{e}</b>"
            ))
            logging.critical(traceback.format_exc())
    else:
        await message.answer("Вы не добавили штрихкоды!")

@dp.message_handler(text = "ℹ️Моя информация")
async def wb_info(message : types.Message):
    wb_userinfo_brand = uh.get(message.from_user.id, "brand")
    wb_userinfo_seller = uh.get(message.from_user.id, "seller")
    wb_userinfo_products = len(uh.get_products(message.from_user.id))

    await message.answer((
        "Ваша информация:\n"
        f"• Бренд: <b>{wb_userinfo_brand}</b>\n"
        f"• Продавец: <b>{wb_userinfo_seller}</b>\n"
        f"Количество добавленных товаров: {wb_userinfo_products}"
    ))

@dp.message_handler(text = "✏️Добавить товары")
async def wb_addProduct(message : types.Message):
    await ProductAddStates.waiting_product_name.set()
    await message.answer((
        "⚠️Внимание! Вы перешли в режим добавления товара!🚧\n"
        "Введите наименование товара:"
    ), reply_markup=menu_keyboard)
    
@dp.message_handler(state=ProductAddStates.waiting_product_name)
async def wb_product_name(message : types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await ProductAddStates.next()
    await message.answer((
        f"Наименование: {message.text}\n"
        "Введите штрихкод:\n"
        """(длиной не более 20 символов, содержащий):
        • исключительно английские или русские буквы, цифры и символы: / * - + @ № % & $ ! = ( ) { } [ ]"""
    ))

@dp.message_handler(state=ProductAddStates.waiting_product_barcode)
async def wb_product_barcode(message : types.Message, state: FSMContext):
    if len(message.text.strip()) >= 20:
        await message.answer("Баркод не должен быть более 20 символов!")
    else:
        try:
            barcode_ready = bargen.create(message.from_user.id, message.text.strip())
            
            await state.update_data(barcode=message.text.strip())
            await state.update_data(barcode_ready=barcode_ready)
            
            brand_data = await state.get_data()
            
            await ProductAddStates.next()
            await message.answer((
                f"Наименование: {brand_data['name']}\n"
                f"Штрихкод: {brand_data['barcode']}\n"
                "Введите артикул:"
            ))
        except Exception as e:
            await message.answer((
                f"Неправильно указан штрихкод!\n"
                f"Текст ошибки: <b>{e}</b>"
            ))

@dp.message_handler(state=ProductAddStates.waiting_product_articul)
async def wb_product_articul(message : types.Message, state: FSMContext):
    forbidden_symbols = ["\\", '.']
    articul = message.text
    if any(c in forbidden_symbols for c in articul):
        await message.answer("Неправильно указан артикул")
    else:
        await state.update_data(articul=message.text)
        brand_data = await state.get_data()
        await ProductAddStates.next()
        uh.product_set(message.from_user.id, brand_data["articul"], {
                "Наименование": brand_data["name"],
                "Штрихкод":     brand_data['barcode'],
                "Артикул":      brand_data['articul']
            }
        )
        await message.answer((
            f"Наименование: {brand_data['name']}\n"
            f"Штрихкод: {brand_data['barcode']}\n"
            f"Артикул: {brand_data['articul']}\n\n"
            
            "Теперь укажите остальные характеристики товара\n"
            "(то, что нужно еще должно быть на маркировке товара)\n"
            "Важно! Заполняйте данные в виде: <u>Цвет: Черный</u>\n"
            "Помните, что ваши обозначения должны соответствовать правилам:\n"
            "   — обозначение не длиннее 30 символов, артикул может содержать:\n"
            "   — только английские или русские буквы, цифры и символы: / * - + @ № % & $ ! = ( ) { } [ ]\n\n"
            "После завершения нажмите на кнопку 'Завершить':)"
        ), reply_markup=product_add_done)

@dp.message_handler(regexp="^[^:]*:[^:]*$", state=ProductAddStates.waiting_product_additional)
async def wb_product_additional(message: types.Message, state: FSMContext):
    brand_data = await state.get_data()
    uid = message.from_user.id
    if message.text.count("\n") > 1:
        await message.answer("Вводите только по одному параметру за раз!")
    else:
        product_key, product_value = message.text.split(":")
        uh.product_add(uid, brand_data["articul"], product_key.strip(), product_value.strip())
        product_params = uh.get_product(uid, brand_data["articul"])
        product_value = f"Наименование: {brand_data['name']}\nШтрихкод: {brand_data['barcode']}\nАртикул: {brand_data['articul']}\n"
        for k,v in product_params.items():
            if k not in ["Наименование", "Штрихкод", "Артикул"]:
                product_value += f"{k}: {v}\n"
        product_value += "\nЧтобы выйти, воспользуйтесь кнопками в клавиатуре"
        await message.answer(product_value)

@dp.message_handler(text="✅Завершить", state=ProductAddStates.waiting_product_additional)
async def wb_product_done(message: types.Message, state: FSMContext):
    uid = message.from_user.id
    brand_data = await state.get_data()
    product_params = uh.get_product(uid, brand_data["articul"])

    label = stickerlabel.label_create(uid, product_params, brand_data["barcode_ready"])
    await message.answer("✅Продукт был успешно сохранен!")

    label_photo = types.InputFile(label)
    await message.answer_photo(
        label_photo, 
        caption="Созданная маркировка. Она будет применятся при создании этикеток",
        reply_markup = home_keyboard
    )
    await state.finish()
    uh.save(uid)