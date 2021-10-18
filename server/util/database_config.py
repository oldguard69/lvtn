import os

import psycopg2
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import util.sql_queries as Q


conn = psycopg2.connect(
    host="localhost",
    database=os.getenv('dbname'),
    user=os.getenv('db_user'),
    password=os.getenv('db_password')
)