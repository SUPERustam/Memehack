#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import urllib.request
import sys
import psycopg2
from telebot.apihelper import util
import ocr
import telebot
import httpx

import config
import util
from db import func_db as fdb


def parse_vk_album(link: str, filename):
    file = open('file.txt', 'w')
    f = subprocess.run(args=f"gallery-dl -g {link}".split(),
                       universal_newlines=True,
                       stdout=file)
    file.close()
    with open('file.txt', 'w') as f:
        a = f.readlines()
        for i in a:
            i += '3434'
    return


def parse_vk_album_another(link: str):
    with Popen(f"gallery-dl -g {link}".split(), stdout=PIPE, universal_newlines=True) as process:
        for i in process.stdout:
            i += '3434'
    return
    # f = subprocess.run(args=f"gallery-dl -g {link}".split(),
    #                    universal_newlines=True,
    #                    stdout=subprocess.PIPE)

    # nmap_lines = f.stdout.splitlines()


def to_vk_album_link(link: str):
    """ Return None when wrong input link"""
    first = link.find('https://vk.com/')
    if first != -1:
        data = {
            'access_token': config.VK_SERVER_ACCESS_KEY,
            'group_id': link[first+15:link.find('?')],
            'fields': 'id',
            'v': 5.154
        }
        r = httpx.post('https://api.vk.com/method/groups.getById', data=data)
        group_id = r.json()['response']['groups'][0]['id']
        return (f"https://vk.com/album-{group_id}_00", int(group_id))


def start_connections():
    # connect to db
    try:
        conn = psycopg2.connect(
            dbname="memehackdb",
            user="postgres",
            host="localhost", # default: mdb
            port=5432,
            password=config.POSTGRES_SERVER_PASSWORD # default: ''
        )
    except psycopg2.Error as error:
        print("I was unable to connect to the database MemeHackDB!\n"
              "Error: {error}")
        sys.exit(1)
    cur = conn.cursor()

    # initialization of ocr
    ocr_cyr, ocr_en = next(ocr.setup_paddleocr())
    return (conn, cur, ocr_cyr, ocr_en)


def process_album(link: str, source_vk: int, conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor, ocr_cyr, ocr_en) -> str:
    count_links = 0
    with Popen(f"gallery-dl -g {link}".split(), stdout=PIPE, universal_newlines=True) as process:
        for img in process.stdout:
            count_links += 1
            img = img[:-1]  # string end up with '\n'
            urllib.request.urlretrieve(img, 'upload_module/pipeline_image.jpg')

            text_ru = util.normalization_text(ocr.image2text(
                ocr_cyr, 'upload_module/pipeline_image.jpg'))
            text_en = util.normalization_text(ocr.image2text(
                ocr_en, 'upload_module/pipeline_image.jpg'))

            fdb.insert_image(cur, vk=img, source_vk=source_vk)
            img_id = cur.fetchone()
            fdb.insert_text(cur, img_id, text_ru, text_en)

    conn.commit()
    return f"Done with {count_links} in {link}"


def close_connections(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor) -> str:
    cur.close()
    conn.close()
    return 'Successful close all db connections'


@util.timeit
def tg_img_upload(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor, bot: telebot.TeleBot):
    chat_item = 0
    storage_chat_id = config.TG_IMG_STORAGE_ID[chat_item]
    bot = telebot.TeleBot(config.TG_TOKEN)

    cur.execute("SELECT id, vk FROM images WHERE tg=''")
    rows = cur.fetchall()

    for row in rows:
        try:
            file_id = bot.send_photo(
                chat_id=storage_chat_id, photo=row[1]).json['photo'][0]['file_id']
            print(row[0], file_id)
        except telebot.apihelper.ApiTelegramException as e:
            print('telebot.apihelper.ApiTelegramException', e)
            print('Telegram error, last writeen object:', file_id,
                  row[0], f'in {chat_item + 1}/{len(config.TG_IMG_STORAGE_ID)} chat')
            conn.commit()
            chat_item += 1
            if chat_item == len(config.TG_IMG_STORAGE_ID):
                chat_item = 0
            storage_chat_id = config.TG_IMG_STORAGE_ID[chat_item]

        cur.execute("UPDATE images SET tg=%s WHERE id=%s", (file_id, row[0]))
    else:
        conn.commit()
    return "Successful process all vk links into Telegram file id"


if "__main__" == __name__:
    conn, cur, ocr_cyr, ocr_en = start_connections()
    # img_upload.tg_img_upload(conn, cur, bot)

    # download albums:
    # print(process_album(*to_vk_album_link('https://vk.com/album-206845783_00'), conn, cur, ocr_cyr, ocr_en))

    # search images
    # ans = fdb.search(cur, input('Search: '))
    # for i in range(len(ans)):
    #     fdb.get_image_by_id(cur, ans[i][0])
    #     urllib.request.urlretrieve(cur.fetchone()[1], f'image{i}.jpg')
    # print(close_connections(conn, cur))
