import time
import os.path as osjoin

from util.sentence_transformer import sentence_transfomer
from util.file_manager import file_manager
from directory import src_dir, src_embeddings_dir


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