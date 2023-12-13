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
