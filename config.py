import os


VK_ACCESS_TOKEN = os.environ['VK_ACCESS_TOKEN']
VK_SERVER_ACCESS_KEY = os.environ['VK_SERVER_ACCESS_KEY']

TG_TOKEN = os.environ['TG_TOKEN']
TG_IMG_STORAGE_ID = [int(os.environ['TG_IMG_STORAGE_ID_1']),
                     int(os.environ['TG_IMG_STORAGE_ID_2']),
                     int(os.environ['TG_IMG_STORAGE_ID_3'])]
AMPLITUDE_API_KEY =  os.environ['AMPLITUDE_API_KEY'],
POSTGRES_SERVER_PASSWORD = os.environ['POSTGRES_SERVER_PASSWORD'] 
