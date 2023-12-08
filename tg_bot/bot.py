#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO:
# 1. Update conn (where and how often?)
# 2. Remove markup keyboard
# 3. with open cursor
# 4. shutdown.py
# 5. Implemet ability to ask for more img for your respond(e.g. "find 5 more pics")
# 6. Implement good design, bot description and links for reaching out to creators


import config
import db.func_db as fdb
import sys

import util
import telebot
from telebot import types
try:
    import psycopg2
except ImportError:
    import psycopg2cffi as psycopg2


import json
import requests
from datetime import datetime
from urllib.parse import urlparse


bot = telebot.TeleBot(config.TG_TOKEN)

# PostgreSQL db connection initialization
try:
    result = urlparse(config.DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    # conn = psycopg2.connect(
    #     dbname="memehackdb",
    #     ser="postgres",
    #     host="memehackdb.internal",
    #     port=5432,
    #     client_encoding="UTF8",
    #     password=config.POSTGRES_SERVER_PASSWORD
    # )
except psycopg2.Error as error:
    print("I was unable to connect to the database MemeHackDB!\n"
          "Error: {error}")
    sys.exit(1)
cur = conn.cursor()


# Languages and responds
languages = {
    '🇷🇺 Русский': 'ru',
    '🇬🇧 English': 'en'
}
selected_language = ''
text_responds = {
    'greet': {
        'ru': 'Добро пожаловать в бота Memehack.\nВведите текстовый запрос:',
        'en': 'Welcome to Memehack bot.\nEnter your text query:',
    },

    'meme_result': {
        'ru': 'Вот, что мне удалось найти!\nВведите новый запрос:',
        'en': 'That\'s all I could find!\nEnter your next query:'
    },

    'no_memes_found': {
        'ru': 'Я не нашел подходящих мемов!\nВведите новый запрос:',
        'en': 'I didn\'t find any memes for that query!\nEnter your next query:',
    }
}


# ------------- ACTIONS LOGGING -------------
actions = []


def send_actions_to_amplitude():
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }

    data = {
        'api_key': config.AMPLITUDE_API_KEY,
        'events': actions,
    }

    response = requests.post("https://api.amplitude.com/2/httpapi",
                             headers=headers, data=json.dumps(data)
                             )

    if response.status_code != 200:
        print("Error:", response.text)
    else:
        print("batch of actions sent, actions:", actions)  # TODO: DELETE
        actions.clear()


def add_action(action_type: str, action: str, message, img_id=None, txt_respond: str = '_'):
    timestamp = int((datetime.now().timestamp() * 1000))
    user_id = message.from_user.id

    if action_type == 'pos':
        if img_id is None:
            detail = txt_respond
        else:
            detail = img_id
    else:
        detail = message.text

    amp_event = {
        "user_id": user_id,
        "event_type": action,
        "time": timestamp,
        "event_properties": {
            "detail": detail
        }
    }
    actions.append(amp_event)

    if len(actions) > 10:
        send_actions_to_amplitude()


# ------------- BOT -------------


@bot.message_handler(commands=['info'])
def info(message):
    pass

# Bot main message-handler functions


@bot.message_handler(commands=['start', 'select_language'])
def start(message):
    fdb.update_or_add_user(cur, message.from_user.id, 'en')
    add_action(action_type='get', action="Get text", message=message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for lang in languages.keys():
        btn = types.KeyboardButton(lang)
        markup.add(btn)
    respond = "🇷🇺 Выберите ваш язык / 🇬🇧 Choose your language"
    bot.send_message(message.from_user.id, respond, reply_markup=markup)
    add_action(action_type='pos', action="Send text",
               message=message, txt_respond=respond)
    bot.register_next_step_handler(message, set_lang)


def set_lang(message):
    add_action(action_type='get', action="Get text", message=message)

    if message.text in languages.keys():
        lang = languages[message.text]
        fdb.update_or_add_user(cur, message.from_user.id, lang)
        respond = text_responds['greet'][lang]
        bot.send_message(message.from_user.id, respond)
        add_action(action_type='pos', action="Send text",
                   message=message, txt_respond=respond)
        # markup = types.ReplyKeyboardRemove() TODO: doesn't work??????
    else:
        respond = "Unknown language! English is set instead.\nEnter your query to find memes:"
        bot.reply_to(message, respond)
        add_action(action_type='pos', action="Send text",
                   message=message, txt_respond=respond)
        fdb.update_or_add_user(cur, message.from_user.id, 'en')
    conn.commit()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    markup = types.ReplyKeyboardRemove()
    selected_language = fdb.get_user_lang(cur, user_id=message.from_user.id)
    fdb.update_or_add_user(cur, message.from_user.id, selected_language)
    add_action(action_type='get', action="Get text", message=message)

    found_memes = fdb.search(cur, message.text)

    for meme in found_memes:
        meme_id = meme[0]
        meme_tg_link = meme[1]
        bot.send_photo(message.from_user.id,
                       photo=meme_tg_link, caption="@memehackbot", reply_markup=markup)
        add_action(action_type='pos', action="Send img",
                   message=message, img_id=meme_id)

    if len(found_memes) != 0:
        meme_result_respond = text_responds['meme_result'][selected_language]
        bot.send_message(message.from_user.id,
                         meme_result_respond, reply_markup=markup)
        add_action(action_type='pos', action="Send text",
                   message=message, txt_respond=meme_result_respond)
    else:
        no_memes_respond = text_responds['no_memes_found'][selected_language]
        bot.send_message(message.from_user.id,
                         no_memes_respond, reply_markup=markup)
        add_action(action_type='pos', action="Send text",
                   message=message, txt_respond=no_memes_respond)
    conn.commit()


bot.polling(none_stop=True, interval=0)


# TODO: close all connection(conn, cur), maybe by shutdown.py, or by hand
conn.close()
