
import psycopg2


def get_image_by_id(cur: psycopg2.extensions.cursor, id: (str | int)):
    cur.execute("SELECT * FROM images WHERE id=%s", (id,))


def insert_image(cur: psycopg2.extensions.cursor, vk: str, vk_small: str = '', tg: str = '', tg_small: str = ''):
    cur.execute("INSERT INTO images (vk, vk_small, tg, tg_small) VALUES (%s, %s, %s, %s)",
                (vk, vk_small, tg, tg_small))


def insert_action():
    # TODO:
    pass


def insert_text(cur: psycopg2.extensions.cursor, img_id: (str | int), text_ru: str, text_en: str):
    cur.execute("INSERT INTO texts (img_id, text_ru, text_en) VALUES (%s, %s, %s)",
                (img_id, text_ru, text_en))


def search(input_text: str) -> list[str | int] | None:
    pass
