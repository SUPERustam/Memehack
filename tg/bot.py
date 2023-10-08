# TODO
# 1. Language
# 2. Log
# 3. Find Function

import telebot
from telebot import types

bot = telebot.TeleBot('6596001732:AAHr6z-mLTJqf0GQ0T0LXzp1IUSNmZ2rICw')

selected_language = ''
text_responds = {
    'greet': {
        'rus': 'Добро пожаловать в бота Memehack.\nВведите свой текстовый запрос:',
        'eng': 'Welcome to Memehack bot.\nEnter your text query:',
    },


    'meme_result': {
        'rus': 'Это все, что мне удалось найти!',
        'eng': 'That\'s all I could find!'
    },

    'no_memes_found': {
        'rus': 'Я не нашел подходящих мемов!',
        'eng': 'I didn\'t find any memes for that query!',
    }
}




@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🇷🇺 Русский')
    btn2 = types.KeyboardButton('🇬🇧 English')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,  "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)
    



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    selected_language = 'rus'

    if message.text == '🇷🇺 Русский':
        selected_language = 'rus'
        greeting = text_responds['greet']['rus']
        bot.send_message(message.from_user.id, greeting)    
    
    elif message.text == '🇬🇧 English':
        selected_language = 'eng'
        greeting = text_responds['greet']['eng']
        bot.send_message(message.from_user.id, greeting)



    elif message.text != 'stop':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.from_user.id, message, reply_markup=markup)

        # found_memes = search(message.text)

        # if len(found_memes) >= 5:
        #     for i in range(5):
        #         bot.send_photo(message.from_user.id, found_memes[i], reply_markup=markup)
        # elif 0 < len(found_memes) < 5:
        #     for i in range(len(found_memes)):
        #         bot.send_photo(message.from_user.id, found_memes[i], reply_markup=markup)
        #         # log_outgoing_img_message()
        bot.send_message(message.from_user.id, 'Here should be memes', reply_markup=markup)
        found_memes = [1, 2]
        


        # Search is over
        meme_result_respond = text_responds['meme_result'][selected_language]
        no_memes_respond = text_responds['no_memes_found'][selected_language]
        if len(found_memes) != 0:
            bot.send_message(message.from_user.id, meme_result_respond, reply_markup=markup)
        else: 
            bot.send_message(message.from_user.id, no_memes_respond, reply_markup=markup)

    else:
        pass


bot.polling(none_stop=True, interval=0)




