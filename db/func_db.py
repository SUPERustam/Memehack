# -*- coding: utf-8 -*-

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    import psycopg2cffi as psycopg2
    from psycopg2cffi import sql
import util


def get_image_by_id(cur: psycopg2.extensions.cursor, id) -> None:
    cur.execute("SELECT * FROM images WHERE id=%s", (id,))


def insert_image(cur: psycopg2.extensions.cursor, vk: str, source_vk: int, tg: str = '', tg_small: str = '') -> None:
    """ also returning id """
    cur.execute("INSERT INTO images (vk, tg, tg_small, source_vk) VALUES (%s, %s, %s, %s) RETURNING id;",
                (vk, tg, tg_small, source_vk))


def insert_text(cur: psycopg2.extensions.cursor, img_id: int, text_ru: str = '', text_en: str = '') -> None:
    cur.execute("INSERT INTO texts (img_id, text_ru, text_en) VALUES (%s, %s, %s)",
                (img_id, text_ru, text_en))


def search(cur: psycopg2.extensions.cursor, input_text: str) -> list:
    # Удалить знаки препинания
    input_text = util.normalization_text(input_text)
    # Удалить лишние пробелы
    input_text = ' '.join(input_text.split())

    cur.execute("""
    SELECT
    	id, tg
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
    """, (input_text, input_text))

    all_texts = cur.fetchall()
    number_list = []

    for tg_link in all_texts:
        if tg_link[1] != '_':
            number_list.append(tg_link)
    return number_list


def get_user_lang(cur: psycopg2.extensions.cursor, user_id: int) -> str:
    cur.execute("SELECT lang FROM users WHERE id = %s", (user_id,))
    lang = cur.fetchone()
    return lang[0] if lang else 'en'


def update_or_add_user(cur: psycopg2.extensions.cursor, user_id: int, lang: str):
    cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
    user_exists = cur.fetchone()
    if user_exists:
        cur.execute("UPDATE users SET lang = %s WHERE id = %s",
                    (lang, user_id))
    else:
        cur.execute("INSERT INTO users (id, lang) VALUES (%s, %s)",
                    (user_id, lang))


# TODO: DELETE IF NOT NEEDED
# old log_action used with postgres db.

# jsonpickle.set_preferred_backend('json')
# jsonpickle.set_encoder_options('json', ensure_ascii=False)

# def log_action(cur: psycopg2.extensions.cursor, action: str, message, img_id = None, txt_respond: str = '_'):
#     timestamp = datetime.now()
#     user_id = message.from_user.id
    # if action == 'pos':
    #     if img_id is None:
    #         detail = json.dumps({'text': txt_respond})
    #     else:
    #         detail = json.dumps({'img_id': img_id})
    # else:
    #     detail = json.dumps({'text': message.text})
    # cur.execute('INSERT INTO actions (time, user_id, img_id, action, detail)'
    #             'VALUES (%s, %s, %s, %s, %s::json)', (timestamp, user_id, img_id, action, detail)
    #             )
    # print(action, user_id, detail)
