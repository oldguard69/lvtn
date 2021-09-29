from os.path import join as osjoin
import numpy as np

from util.file_manager import file_manager
from directory import all_doc_dir, raw_susp_dir, src_dir, susp_stats_dir, susp_dir
from util.plagiarised_doc_maker import PlagiarisedDocMaker


# move data from all_doc_corpus to src and raw_susp corpus
def copy_from_all_doc_corpus(file_list, target_dir, prefix_name, all_doc_dir=all_doc_dir):
    for index, file in enumerate(file_list):
        text = file_manager.read_whole_file(osjoin(all_doc_dir, file))
        file_manager.write_whole_file(osjoin(target_dir, f'{prefix_name}_{index}.txt'), text)

num_of_src_file = 100
file_list = file_manager.listdir_and_sort(all_doc_dir)

np.random.seed(14)
np.random.shuffle(file_list)
copy_from_all_doc_corpus(file_list[:num_of_src_file], src_dir, 'src')
copy_from_all_doc_corpus(file_list[num_of_src_file:], raw_susp_dir, 'susp')


# create suspicious corpus
max_src_files = 5
maker = PlagiarisedDocMaker(raw_susp_dir, susp_dir, susp_stats_dir, src_dir, max_src_files)
maker.make_plagiarised_corpus()