#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import urllib.request
import sys
import psycopg2
import ocr

sys.path.append('.')
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


def to_vk_link(link: str) -> str:
    pass


def start_connections():
    # connect to db
    try:
        conn = psycopg2.connect(
            dbname="memehackdb",
            user="postgres",
            host="mdb",
            port=5432,
            password=''
        )
    except psycopg2.Error as error:
        print("I was unable to connect to the database MemeHackDB!\n"
              "Error: {error}")
        sys.exit(1)
    cur = conn.cursor()

    # initialization of ocr
    ocr_cyr, ocr_en = next(ocr.setup_paddleocr())
    return (conn, cur, ocr_cyr, ocr_en)


def process_album(link: str, connections: tuple) -> str:
    conn, cur, ocr_cyr, ocr_en = connections

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

            fdb.insert_image(cur, vk=img)
            img_id = cur.fetchone()
            fdb.insert_text(cur, img_id, text_ru, text_en)

    conn.commit()
    return f"Done with {count_links} in {link}"


def close_connections(con: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor) -> str:
    cur.close()
    con.close()
    return 'Successful close all db connections'


if "__main__" == __name__:
    connections = start_connections()
    # download albums:
    # print(process_album('https://vk.com/album-206845783_00', connections=connections))
    
    # search images
    # ans = fdb.search(connections[1], input('Search: '))
    # for i in range(len(ans)):
    #     print(ans[i])
    #     urllib.request.urlretrieve(ans[i], f'image{i}.jpg')
    print(close_connections(*connections[:2]))
