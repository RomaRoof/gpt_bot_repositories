import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from hendlers import register_handlers

logging.basicConfig(level=logging.INFO)

GPT_MODEL = "gpt-3.5-turbo"

load_dotenv('config.env')

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

register_handlers(dp)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
