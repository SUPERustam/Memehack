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

bot = telebot.TeleBot('6596001732:AAHr6z-mLTJqf0GQ0T0LXzp1IUSNmZ2rICw')





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
conn.rollback()


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

def get_user_lang(user_id: int):
    cur.execute("SELECT lang FROM users WHERE id = %s", (user_id,))
    lang = cur.fetchone()
    return lang[0] if lang else 'en'

def update_or_add_user(user_id, lang):
    cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
    user_exists = cur.fetchone()
    if user_exists:
        cur.execute("UPDATE users SET lang = %s WHERE id = %s", (lang, user_id))
    else:
        cur.execute("INSERT INTO users (id, lang) VALUES (%s, %s)", (user_id, lang))
    conn.commit()
    




#Bot main functions

@bot.message_handler(commands=['start', 'select_language'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    languages = languages.keys
    for lang in languages:
        btn = types.KeyboardButton(lang)
        markup.add(btn)
    respond = "🇷🇺 Выберите ваш язык / 🇬🇧 Choose your language"
    bot.send_message(message.from_user.id,respond, reply_markup=markup)
    # log_outgoing_message(cur, message, respond)
    bot.register_next_step_handler(message, set_lang)

def set_lang(message):
    if message.text in languages.keys:
        lang = languages[message.text]
        update_or_add_user(message.from_user.id, lang)
        greeting = text_responds['greet'][lang]
        bot.send_message(message.from_user.id, greeting)   
        # log_outgoing_message(cur, message, greeting)
    else:
        respond = "Unknown language! English is set instead.\nEnter your query to find memes:"
        bot.reply_to(message, respond)
        # log_outgoing_message(cur, message, respond)
        update_or_add_user(message.from_user.id, 'en')


@bot.message_handler(commands=['info'])
def info(message):
    pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    selected_language = get_user_lang(message.from_user.id)
     
    if message.text != 'stop':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        found_memes = fdb.search(message.text) 

        for meme_id in found_memes:
            bot.send_photo(message.from_user.id, meme_id, reply_markup=markup)
            # log_outgoing_img(cur, message, meme_id)
        

        meme_result_respond = text_responds['meme_result'][selected_language]
        no_memes_respond = text_responds['no_memes_found'][selected_language]
        if len(found_memes) != 0:
            bot.send_message(message.from_user.id, meme_result_respond, reply_markup=markup)
            # log_outgoing_message(cur, message, meme_result_respond)
        else: 
            bot.send_message(message.from_user.id, no_memes_respond, reply_markup=markup)
            # log_outgoing_message(cur, message, no_memes_respond)
    else:
        pass


bot.polling(none_stop=True, interval=0)