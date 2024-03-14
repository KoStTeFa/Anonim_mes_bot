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
bot = Bot(token='6467512861:AAEPOFhb2HTHrEFvmDSl-H45PPS1QoS1Xbc')
dp = Dispatcher()


async def sen():
    await bot.send_message(883332887, "Пошел нахуй")
    await dp.stop_polling()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
