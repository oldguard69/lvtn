from os.path import join as osjoin
import numpy as np
np.random.seed(14)


from util.file_manager import file_manager
from directory import (all_doc_dir, raw_susp_dir, src_dir,
                       susp_stats_dir, susp_dir, stats_about_file_dir)
from util.plagiarised_doc_maker import PlagiarisedDocMaker

# copy doc from all_doc_corpus to src and raw_susp corpus
def copy_from_all_doc_corpus(file_list, target_dir, prefix_name, all_doc_dir=all_doc_dir):
    for index, file in enumerate(file_list):
        text = file_manager.read_whole_file(osjoin(all_doc_dir, file))
        file_manager.write_whole_file(
            osjoin(target_dir, f'{prefix_name}_{index}.txt'), text
        )

# copy files from all_doc to src and raw_susp
num_of_src_file = 2034
file_list = file_manager.listdir_and_sort(all_doc_dir)
np.random.shuffle(file_list)

copy_from_all_doc_corpus(file_list[:num_of_src_file], src_dir, 'src')
file_manager.write_lines(
    osjoin(stats_about_file_dir, 'src_files_from_all_doc.txt'),
    file_list[:num_of_src_file]
)

copy_from_all_doc_corpus(file_list[num_of_src_file:], raw_susp_dir, 'susp')
file_manager.write_lines(
    osjoin(stats_about_file_dir, 'susp_files_from_all_doc.txt'),
    file_list[num_of_src_file:]
)


# create suspicious corpus
max_src_files = 5
maker = PlagiarisedDocMaker(raw_susp_dir, susp_dir, susp_stats_dir, src_dir, max_src_files)
maker.make_plagiarised_corpus()


# randomly choose 100 susp files to modify plagiarised paragraph
plg_files = file_manager.read_line_by_line(
    osjoin(stats_about_file_dir, 'plg_files_from_raw_susp.txt')
)
np.random.shuffle(plg_files)
file_manager.write_lines(
    osjoin(stats_about_file_dir, 'obfuscation_plg_cases.txt'), plg_files[:100]
)