import os
from os.path import join as osjoin
from time import time

import numpy as np
import pandas as pd

from util.database_config import conn
from util.cosine_similarity import calculate_cosine_similarity
from util.file_manager import file_manager
from util.find_plg_paragraph import find_plagiarised_paragraph, print_stats
import util.sql_queries as Q


src_embeddings_dir = 'embeddings/has_removal/src'
susp_embeddings_dir = 'embeddings/has_removal/susp'
susp_embs_file  = 'susp_35.txt.pk'

classifier = file_manager.pickle_load('model/classifier.pk')
df_columns = ['src_file', 'src_index', 'susp_index', 'cosine_similarity']


def match_susp_emb_with_db(susp_emb, db):
    result = []
    for susp_row in susp_emb:
        for src_row in db:
            cosine = calculate_cosine_similarity(susp_row['embedding'], src_row['embedding'])
            result.append((
                src_row['filename'],
                src_row['index'],
                susp_row['index'],
                cosine
            ))
    return result

def stream_source_embedding(number_of_src_per_chunk):
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

def index_of_plg_sentences(y_pred):
    index = np.nonzero(y_pred)
    return index[0]


start = time()
susp = file_manager.pickle_load(osjoin(susp_embeddings_dir, susp_embs_file))
plg_sents_df = pd.DataFrame()
for src_emb in stream_source_embedding(500):
    df = pd.DataFrame(match_susp_emb_with_db(susp, src_emb), columns=df_columns)
    y_pred = classifier.predict(df.loc[:, ['cosine_similarity']])        
    df = df.iloc[index_of_plg_sentences(y_pred), :]
    plg_sents_df = plg_sents_df.append(df, ignore_index=True)
    print('----')

    
res = find_plagiarised_paragraph(plg_sents_df)
file_manager.write_json('test_1.json', res)
print(time() - start)
