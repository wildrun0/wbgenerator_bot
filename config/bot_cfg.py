import logging
from environs import Env

env = Env()
env.read_env()

try:
    BOT_TOKEN = env.str("BOT_TOKEN")
except:
    logging.critical(".env файл не найден! Создаю новый...")
    logging.critical("Прежде чем использовать бота, необходимо ввести токен в BOT_TOKEN=")

    with open(".env", "w") as f:
        f.write("BOT_TOKEN=token")