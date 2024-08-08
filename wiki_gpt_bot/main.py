import os
import openai
from aiogram import Bot, Dispatcher
import logging

logging.basicConfig(level=logging.INFO)

GPT_MODEL = "gpt-3.5-turbo"

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

if __name__ == '__main__':
    dp.start_polling(bot)
