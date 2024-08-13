import os
from dotenv import load_dotenv
from openai import OpenAI

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
# Определение модели GPT
GPT_MODEL = "gpt-3.5-turbo"
