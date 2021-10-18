from util.database_config import conn
import util.sql_queries as Q

def get_user_by_email(email):
    with conn.cursor() as cur:
        cur.execute(Q.select_a_user, (email, ))
        user = cur.fetchone()
        if user != None:
            user = {
                'id': user[0], 'email': user[1], 
                'password': user[2], 'fullname': user[3]
            }
        return user

def is_user_exist(email):
    with conn.cursor() as cur:
        cur.execute(Q.select_a_user,( email, ))
        return len(cur.fetchall()) != 0

def insert_a_user(email, hash_password, fullname):
    with conn.cursor() as cur:
        cur.execute(Q.insert_a_user, (email, hash_password, fullname))
        conn.commit()
