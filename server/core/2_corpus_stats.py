import os
from os.path import join as osjoin
from collections import defaultdict
from directory import all_doc_dir, src_dir, susp_dir, stats_about_file_dir, susp_stats_dir
from util.file_manager import file_manager

print(f'Total number of documents {len(os.listdir(all_doc_dir))}')
print(f'Total number of documents in src dir {len(os.listdir(src_dir))}')
print(f'Total number of documents in susp dir {len(os.listdir(susp_dir))}')


def stats_plg_type(susp_files):
    result = defaultdict(int)
    for file in file_manager.read_line_by_line(susp_files):
        t = file_manager.read_json(osjoin(susp_stats_dir, f'{file[:-4]}.json'))['type']
        result[t] += 1
    for key, value in result.items():
        print(f'{key}: {value}')


print('Supicious files for training classification model')
stats_plg_type(osjoin(stats_about_file_dir, 'susp_for_train_model.txt'))


print('\nSupicious files for finding plagiarism paragarph')
stats_plg_type(osjoin(stats_about_file_dir, 'susp_for_find_plg_paragraph.txt'))

