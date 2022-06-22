import asyncio
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from handlers import UserHandler, LoggingHandler
from generators import BarcodeGenerator, StickerLabelGenerator

bot = Bot(BOT_TOKEN, parse_mode="HTML")
'''
Хитрый мув (дефолтный): Чтобы воткнуть бота и (например) logginghandler в один луп - 
создаем _сами_ предварительно луп и в него уже пихаем и бота, и то что нужно
В нашем случае - lh.relocate_loggs в app.py
Иначе - никак, нельзя "встроится" в луп бота как это есть в vkbottle
'''
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop = loop, storage=JSONStorage("saved_states.json"))

userhandler = UserHandler()
bargenerator = BarcodeGenerator(userhandler.userdata)
stickerlabelgenerator = StickerLabelGenerator()
lh = LoggingHandler()