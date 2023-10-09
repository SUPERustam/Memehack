# TODO
# 1) two different functions for incoming and outgoing messages
# 2) Пустое поле для исходящих ботовский сообщений
# 3) with open cursor
# 4) shutdown.py


import psycopg2
from psycopg2 import sql
from datetime import datetime

# Log messages (inserting into action db)
def log_incoming_message(cur: psycopg2.extensions.cursor, message):
    timestamp = datetime.fromtimestamp(message.date)
    user_id = message.from_user.id
    action = 'get'
    detail = message 

    cur.execute('INSERT INTO messages (time, user_id, action, detail)' 
        'VALUES (%s, %s, %s, %s::json)', (timestamp, user_id, action, detail)
        )

def log_outgoing_img(cur: psycopg2.extensions.cursor, message, file_id):
    timestamp = datetime.datetime.now()
    user_id = message.from_user.id
    action = 'pos'
    cur.execute('INSERT INTO messages (time, user_id, img_id, action)' 
        'VALUES (%s, %s, %s, %s)', (timestamp, user_id, file_id, action)
        )

def log_outgoing_message(cur: psycopg2.extensions.cursor, message, text: str):
    timestamp = datetime.datetime.now()
    user_id = message.from_user.id
    action = 'pos'
    detail = {'text': text}
    cur.execute('INSERT INTO messages (time, user_id, action detail)' 
        'VALUES (%s, %s, %s, %s::json)', (timestamp, user_id, action, detail)
    )