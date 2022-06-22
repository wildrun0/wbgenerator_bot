import events
from loader import dp, lh
from aiogram import executor

if __name__ == "__main__":
    dp.loop.create_task(lh.relocate_loggs(30))
    executor.start_polling(dp, skip_updates=True)