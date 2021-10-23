import os
import time
from collections import defaultdict
from os.path import join as osjoin

import csv
from pyspark.sql import SparkSession
import pyspark.sql.types as T

from util.file_manager import file_manager
from util.cosine_similarity import calculate_cosine_similarity
from core.directory import (
    src_embeddings_dir, susp_embeddings_dir, susp_stats_dir, csv_dir,
    parquet_train_classifier_dir, train_classifier_log_file
)




spark = SparkSession.builder.appName('test_csv').getOrCreate()
schema = T.StructType([
                       T.StructField('cosine_similarity', T.FloatType(), False),
                       T.StructField('is_plagiarism', T.IntegerType(), False)
])

def convert_from_csv_to_parquet(
    csv_dir, csv_file, parquet_root_dir, parquet_filename
):
    df = spark.read.csv(osjoin(csv_dir, csv_file), header=False, schema=schema)
    df.write.format('parquet').save(osjoin(parquet_root_dir, parquet_filename))
    print(f'done\t', end='')

# stats for a single suspicious file
# convert susp json stats file to stats that can be use for compare susp file with src files
# stats = {'src_name.txt': [{ 'src': set(), 'susp': set() }]
def get_stats_for_a_susp_file(file):
    raw_susp_stats = file_manager.read_json(file)
    stats = defaultdict(list)
    for item in raw_susp_stats['file_stats']:
        para_len = item['paragraph_length']
        start_index_in_src = item['src_start_index']
        insert_index_in_susp = item['susp_insert_index']

        stats[item['src_file']].append({
            'src': set(range(start_index_in_src, start_index_in_src+para_len)),
            'susp': set(range(insert_index_in_susp, insert_index_in_susp+para_len))
        })
    return stats


#  main_stats = {
#     'src_name.txt': [{'src': set(), 'susp': set()}],
#     'src_name.txt': [{'src': set(), 'susp': set()}]
#  }
def is_plagiarism_sentence(src_index, susp_index, src_name, main_stats):
    if src_name in main_stats:
        for index, item in enumerate(main_stats[src_name]):
            if src_index in item['src'] and susp_index in item['susp']:
                main_stats[src_name][index]['src'].remove(src_index)
                main_stats[src_name][index]['susp'].remove(susp_index)
                return 1, main_stats
    return 0, main_stats


def read_embeddings(dir, file):
    return file_manager.pickle_load(osjoin(dir, file))


def stream_source_embeddings_from_pickle(num_of_file=3):
    src_embeddings_files = os.listdir(src_embeddings_dir)
    for start_index in range(0, len(src_embeddings_files), num_of_file):
        source_embeddings = []
        for src_emb in src_embeddings_files[start_index: start_index+num_of_file]:
            source_embeddings.extend(
                file_manager.pickle_load(osjoin(src_embeddings_dir, src_emb))
            )
        yield source_embeddings



susp_list_file = osjoin('..', 'stats_about_files', 'susp_for_train_model.txt')
susp_list = file_manager.read_line_by_line(susp_list_file)
susp_list = [f'embddings_{file}.pk' for file in susp_list]
for susp_embeddings_file in susp_list:
    start = time.time()
    suspicious_embeddings = read_embeddings(susp_embeddings_dir, susp_embeddings_file)

    susp_file_name = susp_embeddings_file[:-7]
    main_stats = get_stats_for_a_susp_file(osjoin(susp_stats_dir,  susp_file_name + '.json'))
    csv_file =  osjoin(csv_dir, susp_file_name + '.csv')
    
    print(f'Convert {susp_file_name}...', end='')

    for source_embeddings in stream_source_embeddings_from_pickle():
        result = []
        for susp_row in suspicious_embeddings:
            for src_row in source_embeddings:
                sim = calculate_cosine_similarity(susp_row['embedding'], src_row['embedding'])                
                is_plg, main_stats = is_plagiarism_sentence(
                    src_row['index'], susp_row['index'], src_row['filename'], main_stats
                )
                result.append((sim, is_plg))

        with open(csv_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(result)
    
    # for performace in read/write dataframe and disk storage
    # convert csv to parquet format and then remove csv file
    convert_from_csv_to_parquet(csv_dir, csv_file, parquet_train_classifier_dir, susp_file_name)
    os.remove(osjoin(csv_dir, csv_file))

    execute_time = round(time.time() - start, 2) / 60
    log_content = f'{susp_embeddings_file} {execute_time} mins'
    file_manager.append_single_line(train_classifier_log_file, log_content)
    print(execute_time, 'mins')