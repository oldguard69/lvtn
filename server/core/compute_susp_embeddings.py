import time
import os.path as osjoin
import os
import numpy as np

from util.sentence_transformer import sentence_transfomer
from util.file_manager import file_manager
from directory import susp_dir, susp_embeddings_dir, susp_embeddings_for_classification, root_dir


def list_doc_in_susp_dir(dir):
    files = os.listdir(dir)
    files = [file for file in files if file[-3:] == 'txt']
    return file_manager.sort_files(files)


# split all susp files into two parts, one for training classification model
# one for finding plagiarism paragraph
all_files = file_manager.listdir_and_sort(susp_dir)
np.random.seed(14)
np.random.shuffle(all_files)
train_classification_susp = all_files[:700]
find_plg_susp = all_files[700:]
file_manager.write_lines(osjoin(root_dir, 'train_classification_susp.txt'), train_classification_susp)
file_manager.write_lines(osjoin(root_dir, 'find_plg_susp.txt'), find_plg_susp)


start = time.time()
# compute embeddings to train classification model
file_per_chunk = 100
i = 0
for index in range(0, len(train_classification_susp), file_per_chunk):
    files = train_classification_susp[index:index+file_per_chunk]

    all_embeddings = []
    for file in files:
        embeddings = sentence_transfomer.compute_embedding_of_a_doc(susp_dir, file)
        all_embeddings.extend(embeddings)
        print(file)

    embedding_file_name = f'susp_embeddings_{i}.pk'
    file_manager.pickle_dump(
        all_embeddings, 
        osjoin(susp_embeddings_for_classification, embedding_file_name)
    )
    i += 1


# compute embeddings of susp file to find plagiarism paragraph
for file in find_plg_susp:
    embeddings = sentence_transfomer.compute_embedding_of_a_doc(susp_dir, file)
    print(file)

    embedding_file_name = f'embeddings_{file}.pk'
    file_manager.pickle_dump(embeddings, osjoin(susp_embeddings_dir, embedding_file_name))

end = time.time()
print(f'Finish in {round((end - start), 5)} second')