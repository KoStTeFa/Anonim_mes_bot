from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.types import InlineKeyboardButton
from aiogram.utils.formatting import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
import logging
import re
from log_writer import save_log
from json_worker import *
import asyncio

logging.basicConfig(level=logging.INFO)
bot = Bot(token='YOUR_SECRET_TOCKEN')
dp = Dispatcher()


# Ожидание отправки анонимного сообщения
@dp.message(CommandStart(
    deep_link=True,  # дикпик
    magic=F.args.regexp(re.compile(r"(\d+)"))
))
async def set_waiting_to_send_message(message: types.Message, command: CommandObject):
    chat_to_send_id = command.args
    if chat_to_send_id.isdigit() and is_address_in_list(int(chat_to_send_id)):
        await save_log(message, "start_waiting_to_write", chat_to_send_id, get_username(int(chat_to_send_id)))

        add_in_order_of_waiting(message.chat.id, int(chat_to_send_id))

        content = Text(
            "Привет 👋\n"
            "Здесь можно отправить анонимное сообщение абсолютно 🎉бесплатно и 👀анонимно\n\n"
            "Можно отправлять сообщение пока только текстом😞\n"
            "Но в последующих обновлениях будут добавляться новые форматы сообщений😁"
        )

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="❌Отмена",
            callback_data="close"
        ))

        await message.answer(**content.as_kwargs(), reply_markup=builder.as_markup())
    else:
        await save_log(message, "bad_address", chat_to_send_id, message.chat.id, message.from_user.username)
        await message.answer("К сожалению, мы не можем отправить сообщение данному пользователю😞\n"
                             "Проверьте🕵️‍♂️, использовали ли вы праильную ссылку")


# Поставить на ожидание повторную отправку сообщения
@dp.callback_query(F.data.startswith("sendAgain_"))
async def send_anonym_message_again(callback: types.CallbackQuery):
    com = CommandObject(prefix="/", command="start", args=f"{callback.data.split("_")[1]}")
    await set_waiting_to_send_message(callback.message, com)
    await callback.answer()


# Отмена ожидания отправки анонимного сообщения
@dp.callback_query(F.data == "close")
async def close_callback(call: types.CallbackQuery):
    await save_log(call.message, "stop_wait")
    if is_message_on_order(call.message.chat.id):
        del_from_order_of_waiting(call.message.chat.id)
    await call.message.delete()
    await call.answer()


# Отправить анонимное сообщение, если есть ожидание или ответить на анонимное сообщение
@dp.message(F.text)
async def send_anonym_message(message: types.Message):
    # Отправка сообщения
    if is_message_on_order(message.chat.id) and is_address_in_list(get_chat(message.chat.id)):
        await save_log(message, "send_anon_message", get_chat(message.chat.id), get_username(get_chat(message.chat.id)))

        mes = await bot.send_message(
            get_chat(message.chat.id),
            f"👀<b>Тебе пришло анонимное сообщение</b>\n\n"
            + message.html_text
            + "\n\n↩️Чтобы ответить свайпни влево",
            parse_mode="html"
        )

        add_new_message_to_ans(mes.message_id, message.chat.id, message.message_id)

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="🔁Отправить ещё раз",
            callback_data=f"sendAgain_{get_chat(message.chat.id)}"
        ))

        await message.answer("✅Ваше сообщение отправлено", reply_markup=builder.as_markup())

        del_from_order_of_waiting(message.chat.id)

        if not is_address_in_list(message.chat.id):
            await message.answer("Чтобы <b>начать получать</b> анонимные сообщения👀 напишите /start", parse_mode="html")

    # Ответ на сообщение
    elif message.reply_to_message is not None and is_mes_in_ans_list(message.reply_to_message.message_id):
        ans_data = get_data_to_ans(message.reply_to_message.message_id)
        await save_log(message, "send_anon_answer", ans_data[0])
        mes = await bot.send_message(
            ans_data[0],
            "👀<b>Тебе пришел ответ</b>\n\n" + message.html_text + "\n\n↩️Чтобы ответить свайпни влево",
            parse_mode="html",
            reply_to_message_id=ans_data[1]
        )
        add_new_message_to_ans(mes.message_id, message.chat.id, message.message_id)
        await message.answer("✅Ваш ответ отправлен")

        if not is_address_in_list(message.chat.id):
            await message.answer("Чтобы <b>начать получать</b> анонимные сообщения👀 напишите /start", parse_mode="html")

    # Иначе просто предложим начать получать анонимные сообщения
    else:
        if message.html_text == "/start":
            await start(message)
        else:
            await save_log(message, "message")
            await message.answer("Чтобы <b>отправить</b> кому-нибудь сообщение💬 пройдите по его персональной ссылке.\n"
                                 "Чтобы <b>начать получать</b> анонимные сообщения👀 напишите /start", parse_mode="html")


# Получить ссылку на анонимку
@dp.message(Command("start"))
async def start(message: types.Message):
    await save_log(message, "satrt_get_message")
    add_new_address(message.chat.id, message.from_user.username)
    content = Text(
        "Привет 👋\n"
        "Хочешь начать получать анонимные сообщения?\n"
        "Вот твоя ссылка:\n\n"
        f"👉 t.me/AnonymousMes_bot?start={message.chat.id}\n\n"
        "Скорей отравляй своим друзьям!"
    )
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Как это работает?", callback_data="how_it_works"))
    builder.row(InlineKeyboardButton(text="🔗Поделиться ссылкой",
                                     url="t.me/share/url?url=Хочешь написать мне анонимное сообщение?\n"
                                         "Тогда держи\n"
                                         f"\n👉 t.me/AnonymousMes_bot?start={message.chat.id}"))
    await message.answer(**content.as_kwargs(), reply_markup=builder.as_markup())


# Нажата кнопка "Как это работает?"
@dp.callback_query(F.data == "how_it_works")
async def how_it_works(calback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔗Поделиться ссылкой",
                                     url="t.me/share/url?url=Хочешь написать мне анонимное сообщение?\n"
                                         "Тогда держи\n"
                                         f"\n👉 t.me/AnonymousMes_bot?start={calback.message.chat.id}"
                                     ))

    content = Text(
        "Вы получаете персональную ссылку\n\n"
        f"👉 t.me/AnonymousMes_bot?start={calback.message.chat.id}\n\n"
        "Можете отправить её своим друзьям🕺 или разместить в своем профиле, чтобы начать получать анонимные сообщения👀"
    )

    await calback.message.edit_text(**content.as_kwargs(), reply_markup=builder.as_markup())
    await calback.answer()


# TODO
# Переслать анонимное сообщение
'''@dp.message()
async def forward_copy_mes(message):
    if is_message_on_order(message.chat.id):
        # await bot.send_message(waiting_to_send[message.chat.id], "Вам пришло новое анонимное сообщение:")
        await message.send_copy(get_chat(message.chat.id))'''


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
