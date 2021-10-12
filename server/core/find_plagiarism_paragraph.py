import os
from os.path import join as osjoin
import numpy as np
import pandas as pd

from util.cosine_similarity import calculate_cosine_similarity
from util.file_manager import file_manager


src_embeddings_dir = ''
susp_embs_dir = ''
plg_dataframe_dir = ''
predited_stats_dir = ''

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

for susp_embs_file in file_manager.read_line_by_line():
    susp = file_manager.pickle_load(susp_embs_dir, susp_embs_file)
    
    plg_sents_df = pd.DataFrame()

    for src_emb in stream_src_embs(5):
        df = pd.DataFrame(match_susp_emb_with_db(susp, src_emb))
        y_pred = classifier.predict(df.loc[:, ['cosine_sim']])

        index = index_of_plg_sentences(y_pred)
        df = df.iloc[index, :]
        plg_sents_df.append(df)

