from os.path import join as osjoin
import random
from util.file_manager import file_manager
import numpy as np
from core.directory import stats_about_file_dir


class PlagiarisedDocMaker:
    def __init__(self, raw_susp_dir, susp_dir, susp_stats_dir, src_dir, max_src_files):
        self.raw_susp_dir = raw_susp_dir
        self.susp_dir = susp_dir
        self.susp_stats_dir = susp_stats_dir
        self.src_dir = src_dir
        self.max_src_files = max_src_files

    def create_plagiarised_file(self, raw_susp_file):
        susp_sentences = file_manager.read_line_by_line(osjoin(self.raw_susp_dir, raw_susp_file))
        file_stats = []
        prev_paragraph_len = 0
        
        # choose a number of src file being plagiarised
        number_of_plg_file = random.randint(1, self.max_src_files)
        src_files = file_manager.listdir_and_sort(self.src_dir)
        # print(f'{raw_susp_file} {number_of_plg_file}')

        # create window (slice of an array) of size window_size
        # each time insertion will be made in the window
        # move window with number_of_plg_file time
        window_size = len(susp_sentences) // number_of_plg_file
        for index in range(number_of_plg_file):
            # choose file in src_dir
            src = random.choice(src_files)
            src_sentences = file_manager.read_line_by_line(osjoin(self.src_dir, src))
                    
            # choose len of  paragraph being plagiarised
            # plg paragraph can be up to one third of the src doc
            # CHANGE THE MAX NUMBER OF PARAGRAPH_LEN
            paragraph_len = random.randint(5, 20)
            
            # choose start index of plgiarised paragraph in src file
            start_index = random.randint(0, len(src_sentences) - paragraph_len)
            plagiarised_paragraph = src_sentences[start_index:start_index+paragraph_len]

            # choose index to insert plagiarised paragraph in susp file
            file_stats_len = len(file_stats)
            if file_stats_len:
                prev_paragraph_len += file_stats[file_stats_len - 1]['paragraph_length']

            # add pre_paragraph_len to make sure the window account the inserted plagiarised paragraph len
            offset = index*window_size + prev_paragraph_len
            insert_index = random.randint(0 + offset, window_size + offset)
            
            # insert plagiarised paragraph into susp sentences
            for i, sent in enumerate(plagiarised_paragraph):
                susp_sentences.insert(insert_index + i, sent)

            # DEBUG
            # print(f'{src} -- {insert_index} -- {start_index} -- {paragraph_len}')
            file_stats.append({
                    'src_file': src, 
                    'paragraph_length': paragraph_len,
                    'src_start_index': start_index, 
                    'susp_insert_index': insert_index
                })
        
        file_manager.write_json(
            osjoin(self.susp_stats_dir, f'{raw_susp_file[:-4]}.json'), 
            {'type': 'automatic', 'file_stats': file_stats}
        )
        file_manager.write_lines(osjoin(self.susp_dir, raw_susp_file), susp_sentences)

    def make_plagiarised_corpus(self):
        total_plagiarism_cases = 0
        total_no_plagiarism_cases = 0
        
        # 300 files là không đạo văn
        # trong 700 files đạo văn, có 210 file có thay đổi
        random.seed(14)
        raw_file_list = file_manager.listdir_and_sort(self.raw_susp_dir)
        np.random.shuffle(raw_file_list)
           
        for raw_susp_file in raw_file_list[:300]:
                file_manager.write_json(
                    osjoin(self.susp_stats_dir, f'{raw_susp_file[:-4]}.json'), 
                    {'type': 'no_plagiarism', 'file_stats': []}
                )
                text = file_manager.read_whole_file(
                        osjoin(self.raw_susp_dir, raw_susp_file)
                    )
                file_manager.write_whole_file(
                    osjoin(self.susp_dir, raw_susp_file),
                    text
                )
                total_no_plagiarism_cases += 1

        for raw_susp_file in raw_file_list[300:]:
            self.create_plagiarised_file(raw_susp_file)
            total_plagiarism_cases += 1

        file_manager.write_lines(
            osjoin(stats_about_file_dir, 'no_plg_files_from_raw_susp.txt'), raw_file_list[:300]
        )
        file_manager.write_lines(
            osjoin(stats_about_file_dir, 'plg_files_from_raw_susp.txt'), raw_file_list[300:]
        )
        print(f'Total plagiarism cases: {total_plagiarism_cases}')
        print(f'Total no plagiarism cases: {total_no_plagiarism_cases}')
