from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

API_TOKEN = "7701492103:AAHzyTt77VQEhTUfBnsEl7qGkzFI5KfYUiQ"

async def start_handler(message: types.Message):
    await message.answer("سلام! ربات آماده است.")

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, Command(commands=["start"]))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
