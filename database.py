import os

if os.getenv("HOME") != '/app':
    from environment import *

DB_HOST = os.getenv('DATABASE_URL').split("/")[2].split(":")[1].split("@")[1]
DB_NAME = os.getenv('DATABASE_URL').split("/")[-1]
DB_USER = os.getenv('DATABASE_URL').split("/")[2].split(":")[0]
DB_PASS = os.getenv('DATABASE_URL').split("/")[2].split(":")[1].split("@")[0]

import psycopg2
import psycopg2.extras

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()
