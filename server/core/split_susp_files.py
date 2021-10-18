from os.path import join as osjoin
from os import listdir
import numpy as np
from collections import defaultdict
from util.file_manager import file_manager
from directory import stats_about_file_dir, susp_stats_dir, susp_dir


def count_susp_type(stats_file=None):
    '''
    Count number of suspicious with its type
    If stats_file is not provided, run stats on susp_dir.
    param:
        stats_file: a file contain susp file name
    '''
    if stats_file is None:
        susp_stats_files = listdir(susp_stats_dir)
        result = defaultdict(int)
        for file in susp_stats_files:
            stats = file_manager.read_json(osjoin(susp_stats_dir, file))['type']
            result[stats] += 1
    else:
        result = defaultdict(int)
        for file in file_manager.read_line_by_line(stats_file):
            stats = file_manager.read_json(
                osjoin(susp_stats_dir, f'{file[:-4]}.json')
            )['type']
            result[stats] += 1
       
        
    for key, value in result.items():
        print(f'Number of {key} cases: {value}')
    


def split_susp_file():
    """
    Split suspicious files into two parts:
      + 500 for training classification model
      + 500 for finding plagiarised paragraph
    """
    np.random.seed(14)
    susp_files = listdir(susp_dir)
    np.random.shuffle(susp_files)

    file_manager.write_lines(
        osjoin(stats_about_file_dir, 'susp_for_train_model.txt'),
        susp_files[:500]
    )
    file_manager.write_lines(
        osjoin(stats_about_file_dir, 'susp_for_find_plg_paragraph.txt'),
        susp_files[500:]
    )
    count_susp_type(osjoin(stats_about_file_dir, 'susp_for_train_model.txt'))
    count_susp_type(osjoin(stats_about_file_dir, 'susp_for_find_plg_paragraph.txt'))

# split_susp_file()

count_susp_type(osjoin(stats_about_file_dir, 'susp_for_train_model.txt'))
count_susp_type(osjoin(stats_about_file_dir, 'susp_for_find_plg_paragraph.txt'))

# current = set()
# for susp in file_manager.read_line_by_line(
#     osjoin(stats_about_file_dir, 'susp_for_find_plg_paragraph.txt')):

#     stats = file_manager.read_json(osjoin(susp_stats_dir, f'{susp[:-4]}.json'))
#     if stats['type'] == 'obfuscation':
#         print(susp)

