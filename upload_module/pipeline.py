#!/usr/bin/python3

import subprocess
import urllib.request
import sys
import time
import psycopg2
import ocr
import telebot
import httpx
from urllib.parse import urlparse

import config
import util
from db import func_db as fdb


@util.timeit
def parse_vk_album(source_vk: str) -> str:
    file = open(f'upload_module/data/{source_vk}.txt', 'w')
    f = subprocess.run(args=f"gallery-dl -g https://vk.com/album-{source_vk}_00".split(),
                       universal_newlines=True,
                       stdout=file)
    file.close()
    return f"Successful parse VK album: upload_module/data/{source_vk}.txt"


def to_vk_album_link(link: str) -> str:  # TODO: fix problem
    """ Return None when wrong input link"""
    first = link.find('https://vk.com/')
    if first != -1:
        group_id = link[first +
                        15:] if link.find('?') == -1 else link[first+15:link.find('?')]
        data = {
            'access_token': config.VK_SERVER_ACCESS_KEY,
            'group_id': group_id,
            'fields': 'id',
            'v': 5.154
        }
        r = httpx.post('https://api.vk.com/method/groups.getById', data=data)
        group_id = r.json()['response']['groups'][0]['id']
        return group_id


def start_connections():
    # connect to db
    try:
        # result = urlparse(config.DATABASE_URL)
        # username = result.username
        # password = result.password
        # database = result.path[1:]
        # hostname = result.hostname
        # port = result.port
        # conn = psycopg2.connect(
        #     database=database,
        #     user=username,
        #     password=password,
        #     host=hostname,
        #     port=port
        # )
        conn = psycopg2.connect(
            dbname="memehackdb",
            user="postgres",
            # host="localhost", # default: mdb
            host='mdb',
            port=5432,
            # password=config.POSTGRES_SERVER_PASSWORD # default: ''
        )
    except psycopg2.Error as error:
        print("I was unable to connect to the database MemeHackDB!\n"
              f"Error: {error}")
        sys.exit(1)
    cur = conn.cursor()

    # initialization of ocr
    ocr_cyr, ocr_en = next(ocr.setup_paddleocr())
    return (conn, cur, ocr_cyr, ocr_en)


def close_connections(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor) -> str:
    cur.close()
    conn.close()
    return 'Successful close all db connections'


@util.timeit
def tg_img_upload(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor, bot: telebot.TeleBot, start_image: int = 0):
    chat_item = 0
    storage_chat_id = config.TG_IMG_STORAGE_ID[chat_item]
    bot = telebot.TeleBot(config.TG_TOKEN)

    cur.execute("SELECT id, vk FROM images WHERE tg=''")
    rows = cur.fetchall()
    file_id = None

    for i, row in enumerate(rows):
        if i < start_image:
            continue
        try:
            file_id = bot.send_photo(
                chat_id=config.TG_IMG_STORAGE_ID[i % 4], photo=row[1]).json['photo'][0]['file_id']
            print(row[0], file_id)
        except telebot.apihelper.ApiTelegramException as e:
            print('telebot.apihelper.ApiTelegramException', e)
            print('Telegram error, last writeen object:', file_id,
                  row[0], f'in {chat_item}/{len(config.TG_IMG_STORAGE_ID)} chat')
            conn.commit()
            time.sleep(5)
        else:
            cur.execute("UPDATE images SET tg=%s WHERE id=%s",
                        (file_id, row[0]))

    conn.commit()
    return "Successful process all vk links into Telegram file id. Added {len(row)}"


def process_photo(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor, ocr_cyr, ocr_en, source_vk: str, image_link: str) -> str:
    sleep_time = 10
    while True:
        try:
            urllib.request.urlretrieve(
                image_link, 'upload_module/cache_image.jpg')
        except urllib.error.URLError as URLError:
            print(
                f"URLError {source_vk=} {image_link=}, sleep({sleep_time})")
            time.sleep(sleep_time)
            sleep_time += 10
            if sleep_time > 50:
                print(
                    'Long wait: more then 50 seconds, added to upload_module/failed_download.txt')
                with open('upload_module/failed_download.txt', 'a') as fail_file:
                    fail_file.write(f"{source_vk} {image_link}\n")
                break
        except Exception as e:
            print(f"{source_vk=} {image_link=}")
            raise e
        else:
            text_ru = util.normalization_text(ocr.image2text(
                ocr_cyr, 'upload_module/cache_image.jpg'))
            text_en = util.normalization_text(ocr.image2text(
                ocr_en, 'upload_module/cache_image.jpg'))
            fdb.insert_image(cur, vk=image_link, source_vk=source_vk)
            img_id = cur.fetchone()
            fdb.insert_text(cur, img_id, text_ru, text_en)
            return f"Successful process {image_link} from {source_vk=}"
    return f"Can't process {image_link} from {source_vk=}"


@util.timeit
def process_album_file(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor, ocr_cyr, ocr_en, source_vk: str, start_image: int = 0) -> str:
    with open(f'upload_module/data/{source_vk}.txt') as image_list:
        for i, link in enumerate(image_list):
            if i < start_image:
                continue

            link = link[:-1]
            sleep_time = 10
            while True:
                try:
                    urllib.request.urlretrieve(
                        link, 'upload_module/cache_image.jpg')
                except urllib.error.URLError as URLError:
                    conn.commit()
                    print(
                        f"URLError {source_vk=} {i=} {link=} conn.commit() done, sleep({sleep_time})")
                    time.sleep(sleep_time)
                    sleep_time += 10
                    if sleep_time > 50:
                        print(
                            'Long wait: more then 50 seconds, added to upload_module/failed_download.txt')
                        with open('upload_module/failed_download.txt', 'a') as fail_file:
                            fail_file.write(f"{source_vk} {link}\n")
                        break
                except Exception as e:
                    conn.commit()
                    print(f"{source_vk=} {i=} {link=} conn.commit() done")
                    raise e
                else:
                    text_ru = util.normalization_text(ocr.image2text(
                        ocr_cyr, 'upload_module/cache_image.jpg'))
                    text_en = util.normalization_text(ocr.image2text(
                        ocr_en, 'upload_module/cache_image.jpg'))
                    fdb.insert_image(cur, vk=link, source_vk=source_vk)
                    img_id = cur.fetchone()
                    fdb.insert_text(cur, img_id, text_ru, text_en)
                    break

        conn.commit()
    return f"Done with {i + 1 - start_image} in https://vk.com/album-{source_vk}_00"


if "__main__" == __name__:
    conn, cur, ocr_cyr, ocr_en = start_connections()

    # search images
    # ans = fdb.search(cur, input('Search: '))
    # for i in range(len(ans)):
    #     fdb.get_image_by_id(cur, ans[i][0])
    #     urllib.request.urlretrieve(cur.fetchone()[1], f'image{i}.jpg')

    for command in sys.argv[1:]:
        try:
            ind = command.find(':')
            if 'tg_img_upload' in command:
                bot = telebot.TeleBot(config.TG_TOKEN)
                if ind == -1:
                    tg_img_upload(conn, cur, bot)
                else:
                    tg_img_upload(conn, cur, bot, int(command[ind + 1:]))
            else:  # from list of links, process images into db
                if ind == -1:
                    print(process_album_file(conn, cur, ocr_cyr, ocr_en, command))
                else:
                    print(process_album_file(conn, cur, ocr_cyr,
                          ocr_en, command, int(command[ind + 1:])))

            # TODO: add option to make list of links from vk album id (using parse_vk_album function, step 1 in plan)

        except KeyboardInterrupt as e:
            print(f'Done {conn.commit()=}')
            sys.exit(1)
        finally:
            print(close_connections(conn, cur))
