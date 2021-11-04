import os
from os.path import join as osjoin
import time

import numpy as np
import pandas as pd

from util.cosine_similarity import calculate_cosine_similarity
from util.file_manager import file_manager
from core.directory import (
    find_plg_log_file, src_embeddings_dir, 
    susp_embeddings_dir, predited_stats_dir, plg_dataframe_dir, stats_about_file_dir
)



def stream_src_embs(num_of_file=3):
    src_embeddings_files = os.listdir(src_embeddings_dir)
    for start_index in range(0, len(src_embeddings_files), 5):
        source_embeddings = []
        for src_emb in src_embeddings_files[start_index: start_index+3]:
            source_embeddings.extend(
                file_manager.pickle_load(osjoin(src_embeddings_dir, src_emb))
            )
        yield source_embeddings


def match_susp_emb_with_db(susp_emb, db):
    result = []
    for susp_row in susp_emb:
        for src_row in db:
            cosine = calculate_cosine_similarity(
                susp_row['embedding'], src_row['embedding']
            )
            result.append(
                (src_row['filename'], src_row['index'],
                susp_row['index'], cosine)
            )
    return result

def index_of_plg_sentences(y_pred):
    index = np.nonzero(y_pred)
    return index[0]

classifier = file_manager.pickle_load(
    '/content/drive/MyDrive/lvtn_data/train_classification_dataset/classifier.pk'
)


df_columns = ['src_file', 'src_index', 'susp_index', 'cosine_similarity']

susp_files = file_manager.read_line_by_line(
    osjoin(stats_about_file_dir, 'susp_for_find_plg_paragraph.txt')
)
susp_files = [f'embeddings_{file}' for file in susp_files]
for susp_embs_file in susp_files:
    start = time.time()
    print(f'{susp_embs_file} --' , end='')
    plg_dataframe_file = osjoin(plg_dataframe_dir, f'{susp_embs_file[:-7]}.parquet')

    susp = file_manager.pickle_load(osjoin(susp_embeddings_dir, susp_embs_file))
    plg_sents_df = pd.DataFrame()
    for src_emb in stream_src_embs(5):
        df = pd.DataFrame(match_susp_emb_with_db(susp, src_emb), columns=df_columns)
        y_pred = classifier.predict(df.loc[:, ['cosine_similarity']])        
        df = df.iloc[index_of_plg_sentences(y_pred), :]
        plg_sents_df = plg_sents_df.append(df, ignore_index=True)
        
    execute_time = round((time.time() - start) / 60, 3) # mins
    log_content = f'{susp_embs_file} {execute_time} mins'
    print(f'{execute_time} mins')

    plg_sents_df.to_parquet(plg_dataframe_file)
    file_manager.append_single_line(find_plg_log_file, log_content)
