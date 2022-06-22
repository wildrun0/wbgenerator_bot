import os
import shutil
import logging
import asyncio
from datetime import datetime

class LoggingHandler():
    def __init__(self):
        self.logging_format = '%(asctime)s [WB_BOT_TG] %(message)s'
        self.default_log_name = "latest.log"
        logging.basicConfig(encoding='utf-8', level=logging.INFO, format=self.logging_format, handlers=[
            logging.FileHandler(self.default_log_name),
            logging.StreamHandler()
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