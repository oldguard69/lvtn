import os
from os.path import join as osjoin
from time import time

import numpy as np
import pandas as pd

from util.cosine_similarity import calculate_cosine_similarity
from util.file_manager import file_manager
from util.find_plg_paragraph import find_plagiarised_paragraph, print_stats

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

def stream_src_embs(num_of_file=3):
    src_embeddings_files = os.listdir(src_embeddings_dir)
    for start_index in range(0, len(src_embeddings_files), num_of_file):
        source_embeddings = []
        for src_emb in src_embeddings_files[start_index: start_index+num_of_file]:
            source_embeddings.extend(
                file_manager.pickle_load(osjoin(src_embeddings_dir, src_emb))
            )
        yield source_embeddings

def index_of_plg_sentences(y_pred):
    index = np.nonzero(y_pred)
    return index[0]


start = time()
susp = file_manager.pickle_load(osjoin(susp_embeddings_dir, susp_embs_file))
plg_sents_df = pd.DataFrame()
for src_emb in stream_src_embs(5):
    df = pd.DataFrame(match_susp_emb_with_db(susp, src_emb), columns=df_columns)
    y_pred = classifier.predict(df.loc[:, ['cosine_similarity']])        
    df = df.iloc[index_of_plg_sentences(y_pred), :]
    plg_sents_df = plg_sents_df.append(df, ignore_index=True)
    print('----')
    
res = find_plagiarised_paragraph(plg_sents_df)
file_manager.write_json('test_2.json', res)
print(time() - start)