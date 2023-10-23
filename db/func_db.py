#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from datetime import datetime
import jsonpickle
import string


def get_image_by_id(cur: psycopg2.extensions.cursor, id: int):
    cur.execute("SELECT * FROM images WHERE id=%s", (id,))


def insert_image(cur: psycopg2.extensions.cursor, vk: str, vk_small: str = '', tg: str = '', tg_small: str = '', source_vk: str = ''):
    cur.execute("INSERT INTO images (vk, vk_small, tg, tg_small, source_vk) VALUES (%s, %s, %s, %s, %s)",
                (vk, vk_small, tg, tg_small, source_vk))

def insert_text(cur: psycopg2.extensions.cursor, img_id: int, text_ru: str = '', text_en: str = ''):
    cur.execute("INSERT INTO texts (img_id, text_ru, text_en) VALUES (%s, %s, %s)",
                (img_id, text_ru, text_en))






def search(cur: psycopg2.extensions.cursor, input_text: str) -> list[int]:
    # Удалить знаки препинания
    input_text = input_text.translate(str.maketrans('', '', string.punctuation))
    # Удалить лишние пробелы
    input_text = ' '.join(input_text.split())

    cur.execute('''
    SELECT
    	tg
    FROM (
    	SELECT
     	img_id,
    	word_similarity(text_ru, %s) + word_similarity(text_en, %s) AS coeff
    	FROM texts
    	) l
    	LEFT JOIN images r
    	ON l.img_id = r.id
    WHERE coeff > 0
    ORDER BY coeff DESC
    LIMIT 5;
    ''', (input_text, input_text))

    all_texts = cur.fetchall()
    number_list = []
    #может попасться элемент NULL, который отображается строкой '_', убираем его
    for row in all_texts:
        for value in row:
            try:
                number = int(value)
                number_list.append(number)
            except ValueError:
                pass

    return number_list




# def add_user(cur: psycopg2.extensions.cursor, user_id: int, lang: str):
#     pass
    
def get_user_lang(cur: psycopg2.extensions.cursor, user_id: int) -> str:
    cur.execute("SELECT lang FROM users WHERE id = %s", (user_id,))
    lang = cur.fetchone()
    return lang[0] if lang else 'en'


def update_or_add_user(cur: psycopg2.extensions.cursor, user_id: int, lang: str):
    cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
    user_exists = cur.fetchone()
    if user_exists:
        cur.execute("UPDATE users SET lang = %s WHERE id = %s", (lang, user_id))
    else:
        cur.execute("INSERT INTO users (id, lang) VALUES (%s, %s)", (user_id, lang))



#TODO: 
# 1)убрать все img_id которые не нужны!!
# 2)Разобраться с encoding, чтобы в db загружался нормально русский текст 
def log_action(cur: psycopg2.extensions.cursor, action: str, message, img_id: int = 0, txt_respond: str = ''):
    timestamp = datetime.now()
    user_id = message.from_user.id
    
    if action == 'pos':
        if img_id == 0:
            detail = jsonpickle.encode({'text': txt_respond})
            cur.execute('INSERT INTO actions (time, user_id, img_id, action, detail)' 
                'VALUES (%s, %s, %s, %s, %s::json)', (timestamp, user_id, img_id, action, detail)
            )
        else:
            detail = jsonpickle.encode({'img_id': img_id})
            cur.execute('INSERT INTO actions (time, user_id, action, detail, img_id)' 
                'VALUES (%s, %s, %s, %s::json, %s)', (timestamp, user_id, action, detail, img_id)
            )   
    
    else:
        detail = jsonpickle.encode({'text': message.text})  
        cur.execute('INSERT INTO actions (time, user_id, action, detail, img_id)' 
            'VALUES (%s, %s, %s, %s::json, %s)', (timestamp, user_id, action, detail, img_id)
        )
    print(action, user_id, detail) #DELETE

