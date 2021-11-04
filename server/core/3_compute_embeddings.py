import time
import os.path as osjoin

import numpy as np

from util.sentence_transformer import sentence_transfomer
from util.file_manager import file_manager
from directory import (
    susp_dir, susp_embeddings_dir, susp_embeddings_for_classification, 
    src_dir, src_embeddings_dir, stats_about_file_dir
)


# compute embeddings for source files
all_files = file_manager.listdir_and_sort(src_dir)
file_per_chunk = 100

start = time.time()
i = 0
for index in range(0, len(all_files), file_per_chunk):
    files = all_files[index:index+file_per_chunk]
    first_file = files[0].split('.')[0]
    last_file = files[len(files) - 1].split('.')[0]

    all_embeddings = []
    for file in files:
        embeddings = sentence_transfomer.compute_embedding_of_a_doc(src_dir, file)
        all_embeddings.extend(embeddings)
        print(file)

    embedding_file_name = f'embeddings_{i}_{first_file}_to_{last_file}.pk'
    file_manager.pickle_dump(all_embeddings, osjoin(src_embeddings_dir, embedding_file_name))
    i += 1

end = time.time()
print(f'Finish in {round((end - start), 5)} second') # 2h35mins




# split all susp files into two parts, 
# one for training classification model
# one for finding plagiarism paragraph  
all_files = file_manager.listdir_and_sort(susp_dir)
np.random.seed(14)
np.random.shuffle(all_files)
train_classification_susp = all_files[:500]
find_plg_susp = all_files[500:]

file_manager.write_lines(
    osjoin(stats_about_file_dir, 'train_classification_susp.txt'), 
    train_classification_susp
)
file_manager.write_lines(
    osjoin(stats_about_file_dir, 'find_plg_susp.txt'), 
    find_plg_susp
)


# compute embeddings to train classification model
start = time.time()
for file in files:
    embeddings = sentence_transfomer.compute_embedding_of_a_doc(susp_dir, file)
    print(file)

    embedding_file_name = f'embeddings_{file}.pk'
    file_manager.pickle_dump(
        embeddings, 
        osjoin(susp_embeddings_for_classification, embedding_file_name)
    )


# compute embeddings of susp file to find plagiarism paragraph
for file in find_plg_susp:
    embeddings = sentence_transfomer.compute_embedding_of_a_doc(susp_dir, file)
    print(file)

    embedding_file_name = f'embeddings_{file}.pk'
    file_manager.pickle_dump(embeddings, osjoin(susp_embeddings_dir, embedding_file_name))

end = time.time()
print(f'Finish in {round((end - start), 5)} second')