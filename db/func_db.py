import psycopg2
from datetime import datetime

def get_image_by_id(cur: psycopg2.extensions.cursor, id: (str | int)):
    cur.execute("SELECT * FROM images WHERE id=%s", (id,))


def insert_image(cur: psycopg2.extensions.cursor, vk: str, vk_small: str = '', tg: str = '', tg_small: str = '', source_vk: str = ''):
    cur.execute("INSERT INTO images (vk, vk_small, tg, tg_small, source_vk) VALUES (%s, %s, %s, %s, %s)",
                (vk, vk_small, tg, tg_small, source_vk))

def insert_text(cur: psycopg2.extensions.cursor, img_id: (str | int), text_ru: str = '', text_en: str = ''):
    cur.execute("INSERT INTO texts (img_id, text_ru, text_en) VALUES (%s, %s, %s)",
                (img_id, text_ru, text_en))





def search(input_text: str) -> list[str | int] | None:
    pass





def get_user_lang(cur: psycopg2.extensions.cursor, user_id: int):
    cur.execute("SELECT lang FROM users WHERE id = %s", (user_id,))
    lang = cur.fetchone()
    return lang[0] if lang else 'en'


def update_or_add_user(cur: psycopg2.extensions.cursor, user_id, lang):
    cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
    user_exists = cur.fetchone()
    if user_exists:
        cur.execute("UPDATE users SET lang = %s WHERE id = %s", (lang, user_id))
    else:
        cur.execute("INSERT INTO users (id, lang) VALUES (%s, %s)", (user_id, lang))




def log_action(cur: psycopg2.extensions.cursor, action: str, message: dict = dict(), img_id: int = 0, text: str = ''):
    timestamp = datetime.datetime.now()
    user_id = message.from_user.id

    if action == 'pos':
        detail = {'text': text}
        if img_id != 0:
            cur.execute('INSERT INTO messages (time, user_id, img_id, action)' 
                'VALUES (%s, %s, %s, %s)', (timestamp, user_id, img_id, action)
            )
        else:
            cur.execute('INSERT INTO messages (time, user_id, action detail)' 
                'VALUES (%s, %s, %s, %s::json)', (timestamp, user_id, action, detail)
            )   
    
    else:
        detail = message
        cur.execute('INSERT INTO messages (time, user_id, action, detail)' 
            'VALUES (%s, %s, %s, %s::json)', (timestamp, user_id, action, detail)
        )