# Импортируем библиотеки:
# Для вызова OpenAI API
import getpass
# Для работы с системными командами
import os

import openai

# Выбираем модель GPT
GPT_MODEL = "gpt-3.5-turbo"

# Помещаем OpenAI ключ в переменную окружения с именем 'OPENAI_API_KEY'
# Привыкайте использовать переменные окружения в своем коде. Это вам позволит легко переносить код на удаленный сервер
# со своим окружением. Также здесь запус происходит через 'python path_to_your_script.py' в терминале, но это не так удобно
# проще запускать через input()
#os.environ["OPENAI_API_KEY"] = getpass.getpass("Введите OpenAI API Key:")
# Ввод ключа API через input()
api_key = input("Введите OpenAI API Key: ")
os.environ["OPENAI_API_KEY"] = api_key

# Проверка наличия ключа API
if not os.environ["OPENAI_API_KEY"]:
    print("API ключ не введен. Завершение программы.")
    exit()

print("API ключ успешно установлен.")

# Запрос к chatGPT
query = 'Когда проходил чемпионат?'
# Создаём объект OpenAI
# openai = OpenAI(
#    api_key=os.environ.get("OPENAI_API_KEY"),
# )
# Отправляем запрос к OpenAI API
response = openai.ChatCompletion.create(
    messages=[
        {'role': 'system', 'content': 'Вы отвечаете на вопросы о Чемпионате мира по крикету 2023'},
        {'role': 'user', 'content': query},
    ],
    model=GPT_MODEL,
    temperature=0,
)
# response = openai.chat.completions.create(
#    messages=[
#        {'role': 'system', 'content': 'Вы отвечаете на вопросы о Чемпионате мира по крикету 2023'},
#        {'role': 'user', 'content': query},
#    ],
#    model=GPT_MODEL,
#    temperature=0,
# )

# Выводим результат
print(response.choices[0].message.content)
