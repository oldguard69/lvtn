import re
import os
from os.path import join as osjoin

import numpy as np
from psycopg2.extras import execute_values

from util.database_config import conn
from util.file_manager import file_manager
import util.sql_queries as Q

def get_number_of_src_files_in_embs_file(first_file, last_file):
    return int(last_file.split('_')[1]) - int(first_file.split('_')[1]) + 1

embs_dir = osjoin('embeddings', 'has_removal', 'src')
all_embs_files = os.listdir(embs_dir)


with conn.cursor() as cur:
    for query in [
        Q.users_table, Q.suspicious_docs_table, 
        Q.source_docs_table, Q.source_embeddings_table
    ]:
        cur.execute(
            query
        )

    print('Create tables successfully')
    conn.commit()
    

for embs_file in sorted(all_embs_files, key=lambda x: int(x.split('_')[1])):
    first_file, last_file = re.findall('src_[0-9]+', embs_file)
    embs = file_manager.pickle_load(osjoin(embs_dir, embs_file))
    i = int(first_file.split('_')[1])
    
    with conn.cursor() as cur:
        for _ in range(
            get_number_of_src_files_in_embs_file(first_file, last_file)
        ):
            src_file = f'src_{i}.txt'
            src_emb = [e for e in embs if e['filename'] == src_file]
            cur.execute(
                Q.insert_a_source_doc, (src_file, len(src_emb))
            )
            source_id = cur.fetchone()[0]

            embedding_data = [
                (source_id, s['index'], s['embedding'].tolist())
                for s in src_emb
            ]
            execute_values(
                cur, Q.insert_embeddings_of_a_source_file, embedding_data
            )

            conn.commit()
            print(f'done for {src_file}')
            i += 1

conn.close()







def stream_source_embedding(number_of_src_per_chunk):
    with conn.cursor() as cur:
        source_ids = cur.execute(Q.select_all_source_docs_id)
    source_ids = sorted([s[0] for s in source_ids])

    for index in range(0, len(source_ids), number_of_src_per_chunk):
        with conn.cursor() as cur:
            cur.execute(
                Q.select_embeddings, 
                source_ids[index:index+number_of_src_per_chunk]
            )
            records = cur.fetchall()
        yield [{
            'filename': r[0],
            'index': r[1],
            'embedding': np.array(r[2])
        } for r in records]
        

# def get_src_from_db(page, offset):
#     with conn.cursor() as cur:
#         cur.execute("SELECT filename, index, embedding FROM src;")
#         records = cur.fetchall()
#     return [{
#         'filename': r[0],
#         'index': r[1],
#         'embedding': np.array(r[2])
#     } for r in records]


# db = sorted(db, key=lambda x: x['index'])
# records = get_src_from_db(0, 0)
# records = sorted(records, key=lambda x: x['index'])


# for i, j in zip(db, records):
#     print('{}: {} ---- {}: {} ---- {}'.format(
#         i['filename'], i['index'], j['filename'], j['index'],
#         calculate_cosine_similarity(i['embedding'], j['embedding'])
#     ))
