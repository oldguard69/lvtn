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

embs_dir = osjoin('embeddings', 'src')
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
    

# for embs_file in sorted(all_embs_files, key=lambda x: int(x.split('_')[1])):
#     first_file, last_file = re.findall('src_[0-9]+', embs_file)
#     embs = file_manager.pickle_load(osjoin(embs_dir, embs_file))
#     i = int(first_file.split('_')[1])
    
#     with conn.cursor() as cur:
#         for _ in range(
#             get_number_of_src_files_in_embs_file(first_file, last_file)
#         ):
#             src_file = f'src_{i}.txt'
#             src_emb = [e for e in embs if e['filename'] == src_file]
#             cur.execute(
#                 Q.insert_a_source_doc, (src_file, len(src_emb))
#             )
#             source_id = cur.fetchone()[0]

#             embedding_data = [
#                 (source_id, s['index'], s['embedding'].tolist())
#                 for s in src_emb
#             ]
#             execute_values(
#                 cur, Q.insert_embeddings_of_a_source_file, embedding_data
#             )

#             conn.commit()
#             print(f'done for {src_file}')
#             i += 1

conn.close()
