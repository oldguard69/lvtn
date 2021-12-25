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


def get_suspicious_docs(user_id):
    with conn.cursor() as cur:
        cur.execute(Q.select_suspicious_docs, (user_id,))
        records = cur.fetchall()
        records = [convert_raw_suspicious_row(r) for r in records]
    return records


def get_a_suspicious_docs(doc_id, user_id):
    with conn.cursor() as cur:
        cur.execute(Q.select_a_suspicious_doc, (int(doc_id), int(user_id)))
        res = cur.fetchone()
    if res != None:
        return convert_raw_suspicious_row(res)
    return res


def convert_raw_suspicious_row(row):
    return {
        'id': row[0],
        'filename': row[1],
        'num_of_sentences': row[2],
        'is_plg': row[3],
        'num_of_plg_sentences': row[4],
        'unique_filename': row[5],
        'user_id': row[6],
        'num_of_plg_paragraphs': row[7]
    }

def insert_a_suspicious_doc(
    filename: str, num_of_sentences: int, is_plg: bool, num_of_plg_sentences: int, 
    unique_filename: str, user_id: int, num_of_plg_paragraphs: int
):
    with conn.cursor() as cur:
        cur.execute(
            Q.insert_a_susp_doc, (
                filename, num_of_sentences, is_plg, 
                num_of_plg_sentences, unique_filename, user_id,
                num_of_plg_paragraphs
            )
        )
        susp_id = cur.fetchone()[0]
        conn.commit()
    return susp_id