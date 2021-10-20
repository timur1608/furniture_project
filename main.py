from telebot import TeleBot, types
from bs4 import BeautifulSoup
import lxml
import config
from urllib import parse
import requests
import os
from random import shuffle

bot = TeleBot(config.token)


def main():
    bot.polling()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, этот бот умеет подбирать мебель под твою комнату\n'
                                      'Просто отправь фото боту, и он автоматически ее подберет')


@bot.message_handler()
def echo_message(message):
    # Use a breakpoint in the code line below to debug your script.
    bot.send_message(message.chat.id, f'Hi, {message.text}')


if __name__ == '__main__':
    main()
