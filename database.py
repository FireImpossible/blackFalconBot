DB_HOST = os.getenv('DATABASE_URL')[91:133]
DB_NAME = os.getenv('DATABASE_URL')[139:]
DB_USER = os.getenv('DATABASE_URL')[11:25]
DB_PASS = os.getenv('DATABASE_URL')[26:90]

import os
import psycopg2
import psycopg2.extras

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()
