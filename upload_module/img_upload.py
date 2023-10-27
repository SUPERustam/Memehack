import sys
sys.path.append("../")
import db.func_db as fdb


import telebot
import psycopg2

import config

storage_chat_id = config.TG_IMG_STORAGE_ID
def tg_img_upload(cur: psycopg2.extensions.cursor, bot: telebot.Telebot, vk_link: str):
    file_id = bot.send_photo(chat_id=storage_chat_id, photo=vk_link).json['photo'][0]['file_id']
    cur.execute("UPDATE images SET tg = %s WHERE vk = %s", (file_id, vk_link))





## second version, which uploads all images which don't have tg_link
 
# def tg_img_upload(cur: psycopg2.extensions.cursor, bot: telebot.Telebot ):
#     storage_chat_id = config.TG_IMG_STORAGE_ID
#     cur.execute("SELECT vk FROM images WHERE tg == '_'")
#     vk_links = cur.fetchall()
#     for url in vk_links:
#         file_id = bot.send_photo(chat_id=storage_chat_id, photo=url).json['photo'][0]['file_id']
#     cur.execute("UPDATE images SET tg = %s", (file_id, ))






