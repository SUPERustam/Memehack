#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO:
# 1. Update conn (where and how often?)
# 2. Remove markup keyboard
# 3. with open cursor
# 4. shutdown.py

import sys
sys.path.append(".")
import config
import db.func_db as fdb
from datetime import datetime

import telebot
from telebot import types
import psycopg2


bot = telebot.TeleBot(config.TG_TOKEN)


# PostgreSQL db connection initialization
try:
    conn = psycopg2.connect(
        dbname="memehackdb",
        user="postgres",
        host="localhost",
        port=5432
    )
except psycopg2.Error as error:
    print("I was unable to connect to the database MemeHackDB!\n"
          "Error: {error}")

# conn.rollback() ?????????
cur = conn.cursor()


# Languages and responds
languages = {
    '🇷🇺 Русский': 'ru',
    '🇬🇧 English': 'en'
}
selected_language = ''
text_responds = {
    'greet': {
        'ru': 'Добро пожаловать в бота Memehack.\nВведите свой текстовый запрос:',
        'en': 'Welcome to Memehack bot.\nEnter your text query:',
    },


    'meme_result': {
        'ru': 'Это все, что мне удалось найти!',
        'en': 'That\'s all I could find!'
    },

    'no_memes_found': {
        'ru': 'Я не нашел подходящих мемов!',
        'en': 'I didn\'t find any memes for that query!',
    }
}


@bot.message_handler(commands=['info'])
def info(message):
    pass


# Bot main functions

@bot.message_handler(commands=['start', 'select_language'])
def start(message):
    print("Executing start\n")  # DELETE

    fdb.update_or_add_user(cur, message.from_user.id, 'en')
    fdb.log_action(cur, action='get', message=message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for lang in languages.keys():
        btn = types.KeyboardButton(lang)
        markup.add(btn)
    respond = "🇷🇺 Выберите ваш язык / 🇬🇧 Choose your language"
    bot.send_message(message.from_user.id, respond, reply_markup=markup)
    fdb.log_action(cur, action='pos', message=message, txt_respond=respond)
    bot.register_next_step_handler(message, set_lang)
    print("Finished start\n")  # DELETE


def set_lang(message):
    print("Executing set_lang\n")  # DELETE
    if message.text in languages.keys():
        lang = languages[message.text]
        fdb.update_or_add_user(cur, message.from_user.id, lang)
        respond = text_responds['greet'][lang]
        bot.send_message(message.from_user.id, respond)
        fdb.log_action(cur, action='pos', message=message, txt_respond=respond)
        print(f'set lang: {lang}\n')  # DELETE
        # markup = types.ReplyKeyboardRemove() TODO: doesn't work??????

    else:
        respond = "Unknown language! English is set instead.\nEnter your query to find memes:"
        bot.reply_to(message, respond)
        fdb.log_action(cur, action='pos', message=message, txt_respond=respond)
        fdb.update_or_add_user(cur, message.from_user.id, 'en')
    conn.commit()
    print(f'Finished set_lang\n')  # DELETE


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    selected_language = fdb.get_user_lang(cur, user_id=message.from_user.id)
    fdb.update_or_add_user(cur, message.from_user.id, selected_language)
    # DELETE
    print(f'Started get_text_messages, users language: {selected_language}\n')
    if message.text != 'stop':  # change to appropriate condition
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # found_memes = fdb.search(message.text)
        # TODO: заглушка, должны быть file_id из предыдущей строки
        found_memes = [1, 2, 3, 4, 5]

        for meme_id in found_memes:
            reply = 'Pic number {}'.format(meme_id)
            # временно, пока нет search
            bot.send_message(message.from_user.id, reply, reply_markup=markup)
            # bot.send_photo(message.from_user.id, meme_id, reply_markup=markup)
            # fdb.log_action(cur, action='pos', message=message, img_id=meme_id)

        if len(found_memes) != 0:
            meme_result_respond = text_responds['meme_result'][selected_language]
            bot.send_message(message.from_user.id,
                             meme_result_respond, reply_markup=markup)
            fdb.log_action(cur, action='pos', message=message,
                           txt_respond=meme_result_respond)
        else:
            no_memes_respond = text_responds['no_memes_found'][selected_language]
            bot.send_message(message.from_user.id,
                             no_memes_respond, reply_markup=markup)
            fdb.log_action(cur, action='pos', message=message,
                           txt_respond=no_memes_respond)
        conn.commit()
    else:
        pass
        # bot.stop_bot()


bot.polling(none_stop=True, interval=0)


# TODO: close all connection(conn, cur), maybe by shutdown.py, or by hand
conn.close()
