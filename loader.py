from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from handlers import UserHandler, LoggingHandler
from generators import BarcodeGenerator, StickerLabelGenerator

bot = Bot(BOT_TOKEN, parse_mode="HTML")

dp = Dispatcher(bot, storage=JSONStorage("saved_states.json"))

userhandler = UserHandler()
bargenerator = BarcodeGenerator(userhandler.userdata)
stickerlabelgenerator = StickerLabelGenerator()
lh = LoggingHandler(name="WB_GEN_BOT")