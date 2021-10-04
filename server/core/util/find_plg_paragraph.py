from pandas import DataFrame
import numpy as np

from cosine_similarity import calculate_cosine_similarity

# Lan luot so sanh tung cau trong susp voi tat ca cau trong src
# Loc ra cac cau dao van
# Sau khi so sanh het voi tat cac cau trong src, dung df co duoc de tim doan dao van


class PlagiarisedParagraphFinder:
    def __init__(self, classifier) -> None:
        self.classifier = classifier

    def sort(self, df: DataFrame) -> DataFrame:
        '''Sort dataframe based on susp_index, src_file src_index'''
        df = df.sort_values(by=['susp_index', 'src_file', 'src_index'])
        return df.reset_index(drop=True)

    def match_susp_embeddings_with_src_embeddings(self, susp_embs, src_embs) -> DataFrame:
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

    def predict_plagiriarised_sentences(self, df: DataFrame) -> DataFrame:
        '''Using classifier to predict df with plagiarised sentences'''
        y_pred = self.classifier.predict(df.loc[:, ['cosine_sim']])
        index = self.index_of_plg_sentences(y_pred)
        return df.loc[index, :]

    def index_of_plg_sentences(self, y_pred) -> list:
        index = np.nonzero(y_pred)
        return index[0]

    def find_plagirised_paragraph(self, df: DataFrame):
        def initialize_current_stats(row):
            current_stats = dict()
            current_stats['src_file'] = row['src_file']
            current_stats['paragraph_len'] = 1
            current_stats['start_index'] = row['src_index']
            current_stats['insert_index'] = row['susp_index']
            return current_stats

        def append_current_stats(result_stats, current_stats):
            result_stats.append({
                'src_file':  current_stats['src_file'],
                'paragraph_len': current_stats['paragraph_len'],
                'start_index': current_stats['start_index'],
                'insert_index': current_stats['insert_index']
            })
            return result_stats

        current_stats = None
        para_len = 1
        result_stats = []
        min_num_of_sentences_between_plg_sents = 2
        for index, row in df.iterrows():
            if current_stats == None:  # first row
                current_stats = initialize_current_stats(row)
                prev_susp_index = row['susp_index']
            else:
                # khoảng cách giữa hai câu đạo văn liên tiếp phải nhỏ hơn 2
                if row['susp_index'] - prev_susp_index <= min_num_of_sentences_between_plg_sents:
                    # câu đang xét và câu phía trước cùng thuộc một văn bản nguồn src_file
                    # tăng độ dài của đoạn đạo văn lên 1,
                    # tăng độ dài của đoạn đạo văn trong văn bản nguồn và nghi ngờ lên khoảng max
                    if row['src_file'] == current_stats['src_file']:
                        para_len += 1
                        current_stats['paragraph_len'] = max(
                            row['src_index'] - current_stats['start_index'],
                            row['susp_index'] - current_stats['insert_index']
                        ) + 1  # +1 vì tính luôn hai câu ngoài cùng

                        prev_susp_index = row['susp_index']
                        # print(f'{index} -- {current_stats} --- {para_len}')
                    # trường hợp có hai susp_index bằng nhau và row['src_file'] != current_stats['src_file']
                    # duyệt câu tiếp theo
                    elif df.loc[index+1, 'susp_index'] == row['susp_index']:
                        continue
                else:
                    # nếu đoạn đao
                    if para_len >= 5:
                        result_stats = append_current_stats(
                            result_stats, current_stats)

                    current_stats = initialize_current_stats(row)
                    prev_susp_index = row['susp_index']

                    para_len = 1
            # lặp hết result, kiểm tra current_stat hợp lệ thì thêm vào result_stats
            if index == len(df) - 1:
                if para_len >= 5:
                    result_stats = append_current_stats(
                        result_stats, current_stats)
        return result_stats

    def find_plagirised_paragraph2(self, df: DataFrame):
        def initialize_current_stats(row):
            current_stats = dict()
            current_stats['src_file'] = row['src_file']
            current_stats['paragraph_len'] = 1
            current_stats['start_index'] = row['src_index']
            current_stats['insert_index'] = row['susp_index']
            return current_stats

        def append_current_stats(result_stats, current_stats):
            result_stats.append({
                'src_file':  current_stats['src_file'],
                'paragraph_len': current_stats['paragraph_len'],
                'start_index': current_stats['start_index'],
                'insert_index': current_stats['insert_index']
            })
            return result_stats

        current_stats = None
        para_len = 1
        result_stats = []
        min_num_of_sentences_between_plg_sents = 2
        for index, row in df.iterrows():
            if current_stats == None:  # first row
                current_stats = dict()
                current_stats[row['src_file']] = {
                    'prev_susp_index': row['susp_index'],
                    'para_len': 1,
                    'stats': initialize_current_stats(row)
                }
            else:
                # khoảng cách giữa hai câu đạo văn liên tiếp phải nhỏ hơn 2
                not_continous_src_files = []
                for src_file in current_stats.keys():
                    if (row['susp_index'] - current_stats[src_file]['prev_susp_index']
                            <= min_num_of_sentences_between_plg_sents):
                        # câu đang xét và câu phía trước cùng thuộc một văn bản nguồn src_file
                        # tăng độ dài của đoạn đạo văn lên 1,
                        # tăng độ dài của đoạn đạo văn trong văn bản nguồn và nghi ngờ lên khoảng max
                        if row['src_file'] == src_file:
                            current_stats[src_file]['para_len'] += 1
                            current_stats[src_file]['stat']['paragraph_len'] = (
                                row['susp_index'] -
                                current_stats['insert_index'] + 1
                            )  # +1 vì tính luôn hai câu ngoài cùng

                            current_stats[src_file]['prev_susp_index'] = row['susp_index']
                        # trường hợp có hai susp_index bằng nhau và row['src_file'] != current_stats['src_file']
                        # duyệt câu tiếp theo
                        elif df.loc[index+1, 'susp_index'] == row['susp_index']:
                            continue
                    else:
                        not_continous_src_files.append(src_file)

                for file in not_continous_src_files:
                    if current_stats[file]['para_len'] >= 5:
                        result_stats = append_current_stats(
                            result_stats, current_stats['stats'])
                    current_stats.pop(file)

            # lặp hết result, kiểm tra current_stat hợp lệ thì thêm vào result_stats
            if index == len(df) - 1:
                if para_len >= 5:
                    result_stats = append_current_stats(
                        result_stats, current_stats)
        return result_stats
