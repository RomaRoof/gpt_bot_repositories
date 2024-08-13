import site

import openai
from aiogram import types, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from gpt_init import GPT_MODEL, client
from base_wiki import titles_from_category, CATEGORY_TITLE


async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Справка"))
    await message.answer("Здравсвуйте. Спросите меня, и возможно я вам отвечу😊",
                         reply_markup=builder.as_markup(resize_keyboard=True))


async def cmd_help(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Справка"))
    await message.answer("Данный бот немного осведомлен в федицинской сфере.\
    Он содержит в себе базу знаний на 1 тысячу строк, выбраных из Википедии по данной сфере",
                         reply_markup=builder.as_markup(resize_keyboard=True))


#async def handle_message(message: types.Message):
#    # Формируем запрос к GPT-3.5-turbo с использованием данных из Википедии
#    prompt = f"""
#    Ты медицинский бот. Пользователь задает вопрос: "{message.text}".
#    Ответь ему подробно и на понятном языке.
#    """
#
#    # Запрос к GPT-3.5-turbo
#    response_gpt = client.chat.completions.create(
#        model=GPT_MODEL,
#        messages=[{"role": "system", "content": "Ты медицинский ассистент."},
#                  {"role": "user", "content": prompt}],
#        temperature=1
#    )
#    answer = response_gpt.choices[0].message.content
#    await message.reply(answer, parse_mode=ParseMode.MARKDOWN)
#
#
def register_handlers(dp: Dispatcher):
    dp.message(Command("start"))(cmd_start)
    dp.message(F.text == "Справка")(cmd_help)
#   dp.message()(handle_message)