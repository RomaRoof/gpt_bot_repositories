# Импортируем библиотеки:
# Для вызова OpenAI API
from openai import OpenAI
# Для работы с системными командами
import os
import getpass

# Выбираем модель GPT
GPT_MODEL = "gpt-3.5-turbo"

# Помещаем OpenAI ключ в переменную окружения с именем 'OPENAI_API_KEY'
# Привыкайте использовать переменные окружения в своем коде. Это вам позволит легко переносить код на удаленный сервер со своим окружением.

os.environ["OPENAI_API_KEY"] = getpass.getpass("Введите OpenAI API Key:")

# Запрос к chatGPT
query = 'Когда проходил чемпионат?'
# Создаём объект OpenAI
openai = OpenAI(
  api_key = os.environ.get("OPENAI_API_KEY"),
)
# Отправляем запрос к OpenAI API
response = openai.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'Вы отвечаете на вопросы о Чемпионате мира по крикету 2023'},
        {'role': 'user', 'content': query},
    ],
    model=GPT_MODEL,
    temperature=0,
)

# Выводим результат
print(response.choices[0].message.content)