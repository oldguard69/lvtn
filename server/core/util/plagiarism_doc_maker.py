import os
import random
from file_manager import file_manager

class PlagiarisedDocMaker:
    def __init__(self, raw_susp_dir, susp_dir, susp_stats_dir, src_dir, max_src_files):
        self.raw_susp_dir = raw_susp_dir
        self.susp_dir = susp_dir
        self.susp_stats_dir = susp_stats_dir
        self.src_dir = src_dir
        self.max_src_files = max_src_files

    def create_plagiarised_file(self, raw_susp_file):
        susp_sentences = file_manager.read_line_by_line(os.path.join(self.raw_susp_dir, raw_susp_file))
        file_stats = []
        prev_paragraph_len = 0
        
        # choose a number of src file being plagiarised
        src_files = file_manager.listdir_and_sort(self.src_dir)
        number_of_plg_file = random.randint(1, self.max_src_files)
        print(f'{raw_susp_file} {number_of_plg_file}')

        # create window (slice of an array) of size window_size
        # each time insertion will be made in the window
        # move window with number_of_plg_file time
        window_size = len(susp_sentences) // number_of_plg_file
        for index in range(number_of_plg_file):
            # choose file in src_dir
            src = random.choice(src_files)
            src_sentences = file_manager.read_line_by_line(os.path.join(self.src_dir, src))
                    
            # choose len of  paragraph being plagiarised
            # plg paragraph can be up to one third of the src doc
            paragraph_len = random.randint(5, len(src_sentences) // 3)
            
            # choose start index of plgiarised paragraph in src file
            start_index = random.randint(0, len(src_sentences) - paragraph_len)
            plagiarised_paragraph = src_sentences[start_index:start_index+paragraph_len]

            # choose index to insert plagiarised paragraph in susp file
            file_stats_len = len(file_stats)
            if file_stats_len:
                prev_paragraph_len += file_stats[file_stats_len - 1]['paragraph_len']

            # add pre_paragraph_len to make sure the window account the inserted plagiarised paragraph len
            offset = index*window_size + prev_paragraph_len
            insert_index = random.randint(0 + offset, window_size + offset)
            
            # insert plagiarised paragraph into susp sentences
            for i, sent in enumerate(plagiarised_paragraph):
                susp_sentences.insert(insert_index + i, sent)

            # DEBUG
            print(f'{src} -- {insert_index} -- {start_index} -- {paragraph_len}')
            file_stats.append({
                    'src_file': src, 
                    'paragraph_len': paragraph_len,
                    'start_index': start_index, 
                    'insert_index': insert_index
                })
        
        file_manager.write_json(
            os.path.join(self.susp_stats_dir, f'{raw_susp_file[:-4]}.json'), 
            {'type': 'automatic', 'file_stat': file_stats}
        )
        file_manager.write_lines(os.path.join(self.susp_dir, raw_susp_file), susp_sentences)

    def make_plagiarised_corpus(self):
        for raw_susp_file in file_manager.listdir_and_sort(self.raw_susp_dir):
            self.create_plagiarised_file(raw_susp_file)


# src files folder
src_dir = '/content/drive/MyDrive/data/test_data/src'

raw_susp_dir = '/content/drive/MyDrive/data/test_data/raw_susp'
susp_dir = '/content/drive/MyDrive/data/test_data/susp'
susp_stats_dir = '/content/drive/MyDrive/data/test_data/susp_stats'

max_src_files = 5

maker = PlagiarisedDocMaker(raw_susp_dir, susp_dir, susp_stats_dir, src_dir, max_src_files)