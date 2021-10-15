from pandas import DataFrame
import numpy as np
from collections import defaultdict

from cosine_similarity import calculate_cosine_similarity

SRC_FILE = 'src_file'
SRC_INDEX = 'src_index'
SUSP_INDEX = 'susp_index'
PARAGRAPH_LENGTH = 'paragraph_length'


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
                'cosine_sim': cosine
            })
    return DataFrame(result)


def initiate_temp_stats(row):
    return {
        'prev_src_index': row['src_index'],
        'prev_susp_index': row['susp_index'],
        'start_index': row['src_index'],
        'insert_index': row['susp_index'],
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
                    temp_stats['prev_src_index']
                susp_index_offset = row[SUSP_INDEX] - \
                    temp_stats['prev_susp_index']

                # <=: nếu khoảng cách giữa hai câu susp liền kề nhỏ hơn 2
                # >: và hai câu này là khác nhau. Vd: 2 câu susp liền kề có index đều là 1.
                # tương tự với điều kiện của src_index_offset
                if susp_index_offset <= 2 and susp_index_offset > 0:
                    if src_index_offset <= 2 and src_index_offset > 0:
                        res[i]['prev_susp_index'] = row[SUSP_INDEX]
                        res[i]['prev_src_index'] = row[SRC_INDEX]
                        res[i]['real_paragraph_length'] = row[SUSP_INDEX] - \
                            temp_stats['insert_index'] + 1
                        res[i]['check_paragraph_length'] += 1
                        # câu đã được xét. Những lần lặp tới của res nếu k thỏa
                        # thì không thêm vào new_temp_stats
                        is_row_approve = True
                    else:
                        # nếu câu không thỏa trong lần lặp cuối thì tạo một temp_stats mới
                        # và coi đây là điểm bắt đầu của một đoạn đạo văn tiềm năng
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
                'src_index': temp_stats['start_index'],
                'susp_index': temp_stats['insert_index'],
                'paragraph_length': temp_stats['real_paragraph_length']
            })
    return final_res


def find_all_plagiarised_paragraph(df):
    res = []
    for src in get_potential_src(df):
        res.extend(find_plagirised_paragraph_with_df_of_a_same_source(
            df.loc[df.src_file == src, :], src)
        )
    res = sorted(res, key=lambda x: x['susp_index'])
    return res


# stats for a single suspicious file
# convert susp json stats file to stats that can be use for compare susp file with src files
# raw_stats = [{'filename': 'src_9.txt', 'paragraph_len': 10, 'start_index': 0, 'insert_index': 0}]
# stats = {'src_name.txt': [{ 'src': set(), 'susp': set() }]
def convert_raw_stats(raw_stats):
    stats = defaultdict(list)
    for item in raw_stats:
        para_len = item['paragraph_length']
        start_index = item['src_index']
        insert_index = item['susp_index']

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


# Độ chính xác được tính là trong tổng số các đoạn đạo văn tìm được, có bao nhiêu đoạn là đúng
def number_of_correct_paragraph_in_a_file(p_pred, p_true):
    """
    so sánh giữa các đoạn được phát hiện và các đoạn thật, có bao nhiêu đoạn được phát hiện là đúng
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


# class PlagiarisedParagraphFinder:
#     def __init__(self, classifier) -> None:
#         self.classifier = classifier

#     def sort(self, df: DataFrame) -> DataFrame:
#         '''Sort dataframe based on susp_index, src_file src_index'''
#         df = df.sort_values(by=['susp_index', 'src_file', 'src_index'])
#         return df.reset_index(drop=True)

#     def match_susp_embeddings_with_src_embeddings(self, susp_embs, src_embs) -> DataFrame:
#         result = []
#         for susp_row in susp_embs:
#             for src_row in src_embs:
#                 cosine = calculate_cosine_similarity(
#                     susp_row['embedding'], src_row['embedding']
#                 )
#                 result.append({
#                     'src_file': src_row['filename'],
#                     'src_index': src_row['index'],
#                     'susp_index': susp_row['index'],
#                     'cosine_sim': cosine
#                 })
#         return DataFrame(result)

#     def predict_plagiriarised_sentences(self, df: DataFrame) -> DataFrame:
#         '''Using classifier to predict df with plagiarised sentences'''
#         y_pred = self.classifier.predict(df.loc[:, ['cosine_sim']])
#         index = self.index_of_plg_sentences(y_pred)
#         return df.loc[index, :]

#     def index_of_plg_sentences(self, y_pred) -> list:
#         index = np.nonzero(y_pred)
#         return index[0]


#     def archive_find_plagirised_paragraph(self, df: DataFrame):
#         def initialize_current_stats(row):
#             current_stats = dict()
#             current_stats['src_file'] = row['src_file']
#             current_stats['paragraph_len'] = 1
#             current_stats['start_index'] = row['src_index']
#             current_stats['insert_index'] = row['susp_index']
#             return current_stats

#         def append_current_stats(result_stats, current_stats):
#             result_stats.append({
#                 'src_file':  current_stats['src_file'],
#                 'paragraph_len': current_stats['paragraph_len'],
#                 'start_index': current_stats['start_index'],
#                 'insert_index': current_stats['insert_index']
#             })
#             return result_stats

#         current_stats = None
#         para_len = 1
#         result_stats = []
#         min_num_of_sentences_between_plg_sents = 2
#         for index, row in df.iterrows():
#             if current_stats == None:  # first row
#                 current_stats = initialize_current_stats(row)
#                 prev_susp_index = row['susp_index']
#             else:
#                 # khoảng cách giữa hai câu đạo văn liên tiếp phải nhỏ hơn 2
#                 if row['susp_index'] - prev_susp_index <= min_num_of_sentences_between_plg_sents:
#                     # câu đang xét và câu phía trước cùng thuộc một văn bản nguồn src_file
#                     # tăng độ dài của đoạn đạo văn lên 1,
#                     # tăng độ dài của đoạn đạo văn trong văn bản nguồn và nghi ngờ lên khoảng max
#                     if row['src_file'] == current_stats['src_file']:
#                         para_len += 1
#                         current_stats['paragraph_len'] = max(
#                             row['src_index'] - current_stats['start_index'],
#                             row['susp_index'] - current_stats['insert_index']
#                         ) + 1  # +1 vì tính luôn hai câu ngoài cùng

#                         prev_susp_index = row['susp_index']
#                         # print(f'{index} -- {current_stats} --- {para_len}')
#                     # trường hợp có hai susp_index bằng nhau và row['src_file'] != current_stats['src_file']
#                     # duyệt câu tiếp theo
#                     elif df.loc[index+1, 'susp_index'] == row['susp_index']:
#                         continue
#                 else:
#                     # nếu đoạn đao
#                     if para_len >= 5:
#                         result_stats = append_current_stats(
#                             result_stats, current_stats)

#                     current_stats = initialize_current_stats(row)
#                     prev_susp_index = row['susp_index']

#                     para_len = 1
#             # lặp hết result, kiểm tra current_stat hợp lệ thì thêm vào result_stats
#             if index == len(df) - 1:
#                 if para_len >= 5:
#                     result_stats = append_current_stats(
#                         result_stats, current_stats)
#         return result_stats
