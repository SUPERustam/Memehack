# TODO
# 1. Update conn (where and how often?)
# 2. Log
# 3. with open cursor
# 4. shutdown.py


import sys
sys.path.append("../")
import db.func_db as fdb

import telebot
from telebot import types

import tg.secrets as secrets
bot = telebot.TeleBot(secrets.TG_TOKEN)





import psycopg2
from psycopg2 import sql
from datetime import datetime


# PostgreSQL db connection initialization
try:
    conn = psycopg2.connect(
        dbname="memehackdb", 
        user="artyom",
        host="localhost", 
        port=5432
        )
except psycopg2.Error as error:
    print("I was unable to connect to the database MemeHackDB!\n"
          "Error: {error}")
    
# conn.rollback() ?????????


cur = conn.cursor()



#Languages and responds

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

    




#Bot main functions

@bot.message_handler(commands=['start', 'select_language'])
def start(message):
    fdb.log_action(cur, action='get', message=message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    languages = languages.keys
    for lang in languages:
        btn = types.KeyboardButton(lang)
        markup.add(btn)
    respond = "🇷🇺 Выберите ваш язык / 🇬🇧 Choose your language"
    bot.send_message(message.from_user.id, respond, reply_markup=markup)
    fdb.log_action(cur, action='pos', message=message, text=respond)
    bot.register_next_step_handler(message, set_lang)

def set_lang(message):
    if message.text in languages.keys:
        lang = languages[message.text]
        fdb.update_or_add_user(message.from_user.id, lang)
        respond = text_responds['greet'][lang]
        bot.send_message(message.from_user.id, respond)
        fdb.log_action(cur, action='pos', message=message, text=respond)   

        
    else:
        respond = "Unknown language! English is set instead.\nEnter your query to find memes:"
        bot.reply_to(message, respond)
        fdb.log_action(cur, action='pos', message=message, text=respond)
        fdb.update_or_add_user(message.from_user.id, 'en')


@bot.message_handler(commands=['info'])
def info(message):
    pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    selected_language = fdb.get_user_lang(message.from_user.id)
     
    if message.text != 'stop':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # found_memes = fdb.search(message.text)
        found_memes = [1,2] #TODO: заглушка, должны быть file_id 

        for meme_id in found_memes:
            bot.send_photo(message.from_user.id, meme_id, reply_markup=markup)
            fdb.log_action(cur, action='pos', message=message, img_id=meme_id, )
        

        meme_result_respond = text_responds['meme_result'][selected_language]
        no_memes_respond = text_responds['no_memes_found'][selected_language]
        if len(found_memes) != 0:
            bot.send_message(message.from_user.id, meme_result_respond, reply_markup=markup)
            fdb.log_action(cur, action='pos', message=message, text=meme_result_respond)
        else: 
            bot.send_message(message.from_user.id, no_memes_respond, reply_markup=markup)
            fdb.log_action(cur, action='pos', message=message, text=no_memes_respond)
    else:
        pass

#TODO: close all connection(conn, cur), maybe by shutdown.py, or by hand
bot.polling(none_stop=True, interval=0)