import os
import shutil
import logging
import asyncio
from datetime import datetime

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - [WB_BOT_TG] - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LoggingHandler():
    def __init__(self):
        self.default_log_name = "latest.log"
        console_stream = logging.StreamHandler()
        console_stream.setFormatter(CustomFormatter())
        logging.basicConfig(encoding='utf-8', level=logging.INFO, handlers=[
            logging.FileHandler(self.default_log_name),
            console_stream
        ])

    def clean_log_file(self) -> None:
        open(self.default_log_name, "w").close()

    async def relocate_loggs(self, sleep_time) -> None:
        while 1:
            await asyncio.sleep(sleep_time)
            dt = datetime.now()
            if dt.hour == 0 and dt.minute == 0:
                logging.info("latest.log was moved to logs/")
                date_string = dt.strftime('%d-%m-%Y')
                filelog_name = f"log{date_string}.txt"
                destination = f"logs/{filelog_name}"
                
                if not os.path.exists("logs"):
                    os.mkdir("logs")
                    
                if os.name == "posix":
                    os.replace(self.default_log_name, destination)
                else:
                    shutil.copy(self.default_log_name, destination)
                    
                self.clean_log_file()