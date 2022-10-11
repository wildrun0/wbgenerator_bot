#!/usr/bin/python
from loader import dp
from aiogram import executor
import events

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)