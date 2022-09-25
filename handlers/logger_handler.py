import logging
from pathlib import Path
import logging.handlers as handlers

class CustomFormatter(logging.Formatter):
    def __init__(self, name):
        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        self.format_str = f"%(asctime)s - [{name}] - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

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
    def __init__(self, name):
        self.default_log_name = f"{name}.log"
        self.default_logs_folder = Path("logs")
        self.latest_log_path = Path(self.default_logs_folder, self.default_log_name)
        self.default_logs_folder.mkdir(exist_ok=True)
        customformat = CustomFormatter(name)
        
        filestream = handlers.TimedRotatingFileHandler(self.latest_log_path, when="midnight", interval=1, encoding="utf8")
        filestream.suffix = "%Y-%m-%d"
        filestream.setFormatter(
            logging.Formatter(customformat.format_str)
        )
        
        console_stream = logging.StreamHandler()
        console_stream.setFormatter(customformat)
        
        logging.basicConfig(encoding='utf-8', level=logging.INFO, handlers=[
            filestream,
            console_stream
        ])