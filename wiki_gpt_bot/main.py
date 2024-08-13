import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

# from base_wiki import initialize_wiki_base
from hendlers import register_handlers

logging.basicConfig(level=logging.INFO)

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

#initialize_wiki_base()
register_handlers(dp)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
