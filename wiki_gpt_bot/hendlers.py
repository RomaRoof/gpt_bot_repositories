from aiogram import types, Dispatcher
from aiogram.filters.command import Command

from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Справка"))
    await message.answer("Здравсвуйте. Спросите меня, и возможно я вам отвечу😊",
                         reply_markup=builder.as_markup(resize_keyboard=True))


def register_handlers(dp: Dispatcher):
    dp.message(Command("start"))(cmd_start)
