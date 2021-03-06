from pandas import DataFrame
import numpy as np
from collections import defaultdict
import pandas as pd

from util.cosine_similarity import calculate_cosine_similarity
from util.stream_source_embeddings import (
    stream_source_embedding_from_database, 
    stream_source_embeddings_from_pickle
)

SRC_FILE = 'src_file'
SRC_INDEX = 'src_index'
SUSP_INDEX = 'susp_index'
PARAGRAPH_LENGTH = 'paragraph_length'
df_columns = ['src_file', 'src_index', 'susp_index', 'cosine_similarity']

def match_susp_embeddings_with_src_embeddings(susp_embs, src_embs) -> DataFrame:
    result = []
    for susp_row in susp_embs:
        for src_row in src_embs:
            cosine = calculate_cosine_similarity(
                susp_row['embedding'], src_row['embedding']
            )
            result.append({
                'src_file': src_row['filename'],
                'src_index': src_row['index'],
                'susp_index': susp_row['index'],
                'cosine_similarity': cosine
            })
    return DataFrame(result)

def index_of_plg_sentences(y_pred):
    index = np.nonzero(y_pred)
    return index[0]

def get_dataframe_contain_plagiarised_sentences(susp_embeddings, classifier) -> DataFrame:
    plg_sents_df = pd.DataFrame()
    i = 0
    for src_emb in stream_source_embeddings_from_pickle(3):
    # for src_emb in stream_source_embedding_from_database(300):
        df = pd.DataFrame(
            match_susp_embeddings_with_src_embeddings(susp_embeddings, src_emb), 
            columns=df_columns
        )
        y_pred = classifier.predict(df.loc[:, ['cosine_similarity']])        
        df = df.iloc[index_of_plg_sentences(y_pred), :]
        plg_sents_df = plg_sents_df.append(df, ignore_index=True)
        print(i, end=' ')
        i += 1
    return plg_sents_df


def initiate_temp_stats(row):
    return {
        'prev_src_index': row['src_index'],
        'prev_susp_index': row['susp_index'],
        'src_start_index': row['src_index'],
        'susp_insert_index': row['susp_index'],
        'real_paragraph_length': 1,
        'check_paragraph_length': 1
    }

def get_potential_src(df):
    temp = df.groupby('src_file').agg({'src_index': list, 'susp_index': list})
    return list(temp.loc[temp.susp_index.apply(len) >= 5, :].index)


def sort_dataframe(df: DataFrame) -> DataFrame:
    '''Sort dataframe based on susp_index, src_file src_index'''
    df = df.sort_values(by=['susp_index', 'src_file', 'src_index'])
    return df.reset_index(drop=True)


def find_plagirised_paragraph_with_df_of_a_same_source(df, src_file):
    '''df contains plg sentences belong to a source file.'''
    df = sort_dataframe(df)
    res = []
    is_first_iter = True
    for index, row in df.iterrows():
        if is_first_iter:
            res.append(initiate_temp_stats(row))
            is_first_iter = False
        else:
            new_temp_stats = []
            is_row_approve = False
            is_last = False

            for i, temp_stats in enumerate(res):
                if i == len(res) - 1:
                    is_last = True

                src_index_offset = row[SRC_INDEX] - \
                    temp_stats['prev_src_index'] - 1
                susp_index_offset = row[SUSP_INDEX] - \
                    temp_stats['prev_susp_index'] - 1

                # <=: n???u kho???ng c??ch gi???a hai c??u susp li???n k??? nh??? h??n 2
                # >=: v?? hai c??u n??y l?? kh??c nhau. Vd: 2 c??u susp li???n k??? c?? index ?????u l?? 1.
                # t????ng t??? v???i ??i???u ki???n c???a src_index_offset
                if susp_index_offset <= 2 and susp_index_offset >= 0:
                    if src_index_offset <= 2 and src_index_offset >= 0:
                        res[i]['prev_susp_index'] = row[SUSP_INDEX]
                        res[i]['prev_src_index'] = row[SRC_INDEX]
                        res[i]['real_paragraph_length'] = row[SUSP_INDEX] - \
                            temp_stats['susp_insert_index'] + 1
                        res[i]['check_paragraph_length'] += 1
                        # c??u ???? ???????c x??t. Nh???ng l???n l???p t???i c???a res n???u k th???a
                        # th?? kh??ng th??m v??o new_temp_stats
                        is_row_approve = True
                    else:
                        # n???u c??u kh??ng th???a trong l???n l???p cu???i th?? t???o m???t temp_stats m???i
                        # v?? coi ????y l?? ??i???m b???t ?????u c???a m???t ??o???n ?????o v??n ti???m n??ng
                        if not is_row_approve and is_last:
                            is_row_approve = True
                            new_temp_stats.append(initiate_temp_stats(row))

                else:
                    if not is_row_approve and is_last:
                        is_row_approve = True
                        new_temp_stats.append(initiate_temp_stats(row))

            if len(new_temp_stats):
                res.extend(new_temp_stats)

    final_res = []
    for temp_stats in res:
        if temp_stats['check_paragraph_length'] >= 5 and temp_stats['real_paragraph_length'] >= 5:
            final_res.append({
                'src_file': src_file,
                'src_start_index': temp_stats['src_start_index'],
                'susp_insert_index': temp_stats['susp_insert_index'],
                'paragraph_length': temp_stats['real_paragraph_length']
            })
    return final_res


def find_plagiarised_paragraph(df):
    res = []
    for src in get_potential_src(df):
        res.extend(find_plagirised_paragraph_with_df_of_a_same_source(
            df.loc[df.src_file == src, :], src)
        )
    res = sorted(res, key=lambda x: x['susp_insert_index'])
    return res


# stats for a single suspicious file
# convert susp json stats file to stats that can be use for compare susp file with src files
# raw_stats = [{'filename': 'src_9.txt', 'paragraph_len': 10, 'start_index': 0, 'insert_index': 0}]
# stats = {'src_name.txt': [{ 'src': set(), 'susp': set() }]
def convert_raw_stats(raw_stats):
    stats = defaultdict(list)
    for item in raw_stats:
        para_len = item['paragraph_length']
        start_index = item['src_start_index']
        insert_index = item['susp_insert_index']

        stats[item['src_file']].append({
            'src': set(range(start_index, start_index+para_len)),
            'susp': set(range(insert_index, insert_index+para_len))
        })
    return stats


def is_intersection_gte(
    predicted_set: set,
    true_set: set,
    percentage_threshold: float
) -> bool:
    return len(predicted_set.intersection(true_set)) / len(true_set) >= percentage_threshold


# ????? ch??nh x??c ???????c t??nh l?? trong t???ng s??? c??c ??o???n ?????o v??n t??m ???????c, c?? bao nhi??u ??o???n l?? ????ng
def number_of_correct_paragraph_in_a_file(p_pred, p_true):
    """
    so s??nh gi???a c??c ??o???n ???????c ph??t hi???n v?? c??c ??o???n th???t, c?? bao nhi??u ??o???n ???????c ph??t hi???n l?? ????ng
    param:
        p_pred: convert_raw_stats(res)
        p_true: convert_raw_stats(real_stats)
    return:
        number of correct identified plagiarised paragraphs in p_pred compare to p_true
    """
    containment_percentage = 0.8
    total_correct_paragraph = 0
    for src_file in p_pred.keys():
        if src_file in p_true:
            for paragraph in p_pred[src_file]:
                p_src = paragraph['src']
                p_susp = paragraph['susp']

                is_correct = False
                for true_paragraph in p_true[src_file]:
                    if is_intersection_gte(p_src, true_paragraph['src'], containment_percentage) and \
                       is_intersection_gte(p_susp, true_paragraph['susp'], containment_percentage):
                        is_correct = True
                        break
                if is_correct:
                    total_correct_paragraph += 1
    return total_correct_paragraph

def print_stats(stats, column_size=25):
    def padding_space(string,  column_size=25):
        string = str(string)
        t = column_size - len(string)
        r = int(t // 2)
        if t % 2:
            s = ' '*r + string + ' '*(r+1)
        else:
            s = ' '*r + string + ' '*r   
        return s

    width = column_size * 4 + 5
    print('='*width)
    for i in ['src_file', 'src_start_index', 'susp_insert_index', 'paragraph_length']:
        print('|' + padding_space(i, column_size), end='')
    print('|')
    print('='*width)

    for item in stats:
        for key in ['src_file', 'src_start_index', 'susp_insert_index', 'paragraph_length']:
            print("|" + padding_space(item[key], column_size), end='')
        print('|')
        print('='*width)
