import ast
import os

import pandas as pd
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
from scipy import spatial

dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path)
# Определение модели GPT
GPT_MODEL = "gpt-3.5-turbo"
# Токен OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-ada-002"  # Модель токенизации от OpenAI
# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

df = pd.read_csv("D:\Рома Учеба\Founder\DSHomeWork\gpt_bot_repositories\wiki_gpt_bot\knowledge_base\med_pediatrics.csv")
df['embedding'] = df['embedding'].apply(ast.literal_eval)


# Функция поиска
def strings_ranked_by_relatedness(
        query: str,  # пользовательский запрос
        df: pd.DataFrame,  # DataFrame со столбцами text и embedding (база знаний)
        relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),  # функция схожести, косинусное расстояние
        top_n: int = 100  # выбор лучших n-результатов
) -> tuple[list[str], list[
    float]]:  # Функция возвращает кортеж двух списков, первый содержит строки, второй - числа с плавающей запятой
    """Возвращает строки и схожести, отсортированные от большего к меньшему"""

    # Отправляем в OpenAI API пользовательский запрос для токенизации
    query_embedding_response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )

    # Получен токенизированный пользовательский запрос
    query_embedding = query_embedding_response.data[0].embedding

    # Сравниваем пользовательский запрос с каждой токенизированной строкой DataFrame
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]

    # Сортируем по убыванию схожести полученный список
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)

    # Преобразовываем наш список в кортеж из списков
    strings, relatednesses = zip(*strings_and_relatednesses)

    # Возвращаем n лучших результатов
    return strings[:top_n], relatednesses[:top_n]


# с этой функцией мы уже знакомы
def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Возвращает число токенов в строке для заданной модели"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


# Функция формирования запроса к chatGPT по пользовательскому вопросу и базе знаний
def query_message(
        query: str,  # пользовательский запрос
        df: pd.DataFrame,  # DataFrame со столбцами text и embedding (база знаний)
        model: str,  # модель
        token_budget: int  # ограничение на число отсылаемых токенов в модель
) -> str:
    """Возвращает сообщение для GPT с соответствующими исходными текстами, извлеченными из фрейма данных (базы знаний)."""
    strings, relatednesses = strings_ranked_by_relatedness(query,
                                                           df)  # функция ранжирования базы знаний по пользовательскому запросу
    # Шаблон инструкции для chatGPT
    message = 'Use the below articles on the 2022 Winter Olympics to answer the subsequent question. If the answer cannot be found in the articles, write "I could not find an answer."'
    # Шаблон для вопроса
    question = f"\n\nQuestion: {query}"

    # Добавляем к сообщению для chatGPT релевантные строки из базы знаний, пока не выйдем за допустимое число токенов
    for string in strings:
        next_article = f'\n\nWikipedia article section:\n"""\n{string}\n"""'
        if (num_tokens(message + next_article + question, model=model) > token_budget):
            break
        else:
            message += next_article
    return message + question


def ask(
        query: str,  # пользовательский запрос
        df: pd.DataFrame = df,  # DataFrame со столбцами text и embedding (база знаний)
        model: str = GPT_MODEL,  # модель
        token_budget: int = 4096 - 500,  # ограничение на число отсылаемых токенов в модель
        print_message: bool = False,  # нужно ли выводить сообщение перед отправкой
) -> str:
    """Отвечает на вопрос, используя GPT и базу знаний."""
    # Формируем сообщение к chatGPT (функция выше)
    message = query_message(query, df, model=model, token_budget=token_budget)
    # Если параметр True, то выводим сообщение
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "You answer questions about the 2022 Winter Olympics."},
        {"role": "user", "content": message},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
        # гиперпараметр степени случайности при генерации текста. Влияет на то, как модель выбирает следующее слово в последовательности.
    )
    response_message = response.choices[0].message.content
    return response_message

