import os
from os.path import join as osjoin

import numpy as np

from util.file_manager import file_manager
from util.database_config import conn, Q

def stream_source_embedding_from_database(number_of_src_per_chunk):
    with conn.cursor() as cur:
        cur.execute(Q.select_all_source_docs_id)
        source_ids = cur.fetchall()
    source_ids = sorted([s[0] for s in source_ids])

    for index in range(0, len(source_ids), number_of_src_per_chunk):
        with conn.cursor() as cur:
            cur.execute(
                Q.select_embeddings, 
                (tuple(source_ids[index:index+number_of_src_per_chunk]), )
            )
            records = cur.fetchall()
        yield [{
            'filename': r[0],
            'index': r[1],
            'embedding': np.array(r[2])
        } for r in records]


src_embeddings_dir = './core/embeddings/src'
def stream_source_embeddings_from_pickle(num_of_file=3):
    src_embeddings_files = os.listdir(src_embeddings_dir)
    for start_index in range(0, len(src_embeddings_files), num_of_file):
        source_embeddings = []
        for src_emb in src_embeddings_files[start_index: start_index+num_of_file]:
            source_embeddings.extend(
                file_manager.pickle_load(osjoin(src_embeddings_dir, src_emb))
            )
        yield source_embeddings