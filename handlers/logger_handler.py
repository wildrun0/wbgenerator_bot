import os
import shutil
import logging
import asyncio
from pathlib import Path
from datetime import datetime

class CustomFormatter(logging.Formatter):
    def __init__(self):
        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        self.format_str = "%(asctime)s - [WB_BOT_TG] - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

        self.FORMATS = {
            logging.DEBUG: grey + self.format_str + reset,
            logging.INFO: grey + self.format_str + reset,
            logging.WARNING: yellow + self.format_str + reset,
            logging.ERROR: red + self.format_str + reset,
            logging.CRITICAL: bold_red + self.format_str + reset
        }


    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LoggingHandler():
    def __init__(self):
        self.default_log_name = "latest.log"
        self.default_logs_folder = Path("logs")
        self.latest_log_path = Path(self.default_logs_folder, self.default_log_name)
        self.default_logs_folder.mkdir(exist_ok=True)
        customformat = CustomFormatter()
        
        filestream = logging.FileHandler(self.latest_log_path)
        filestream.setFormatter(
            logging.Formatter(customformat.format_str)
        )
        
        console_stream = logging.StreamHandler()
        console_stream.setFormatter(customformat)
        
        logging.basicConfig(encoding='utf-8', level=logging.INFO, handlers=[
            filestream,
            console_stream
        ])


    async def relocate_logs(self, sleep_time: int = 3600) -> None:
        while 1:
            dt = datetime.now()
            if dt.hour == 0:
                logging.warning("latest.log was renewed")
                date_string = dt.strftime('%d-%m-%Y')
                
                filelog_name = f"{date_string}.log.txt"
                new_log_path = Path(self.default_logs_folder, filelog_name)
                    
                if os.name == "posix":
                    self.latest_log_path.rename(new_log_path)
                else: #windows не даст удалить (переименовать) файл пока он открыт у нас
                    shutil.copy(self.latest_log_path, new_log_path)
                    
                self.latest_log_path.write_text("")
            await asyncio.sleep(sleep_time)
