DB_HOST = "ec2-50-16-108-41.compute-1.amazonaws.com"
DB_NAME = "d89ra8pgoll1n0"
DB_USER = "uqspjisevftviw"
DB_PASS = "6d8061c79dabe16cf32c02eefa4a3757f5c25e0531ac6a4762d273130ee0f823"

import psycopg2
import psycopg2.extras

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()
