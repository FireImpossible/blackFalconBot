import os

if os.getenv("HOME") != '/app':
    from environment import *

DB_HOST = os.getenv('DATABASE_URL')[91:131]
DB_NAME = os.getenv('DATABASE_URL')[137:]
DB_USER = os.getenv('DATABASE_URL')[11:25]
DB_PASS = os.getenv('DATABASE_URL')[26:90]

import psycopg2
import psycopg2.extras

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()
