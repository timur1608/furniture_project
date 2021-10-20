from bs4 import BeautifulSoup
from aiogram import Bot, types
import lxml
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config
from urllib import parse
import requests
import os
from random import shuffle

bot = Bot(config.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет, этот бот умеет подбирать мебель под твою комнату\n'
                                            'Просто отправь фото боту, и он автоматически ее подберет')


@dp.message_handler()
async def echo_message(message):
    # Use a breakpoint in the code line below to debug your script.
    await bot.send_message(message.chat.id, f'Hi, {message.text}')


if __name__ == '__main__':
    executor.start_polling(dp)
