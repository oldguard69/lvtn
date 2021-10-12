import os

from directory import all_doc_dir, src_dir, raw_susp_dir, susp_dir


print(f'Total number of documents {len(os.listdir(all_doc_dir))}')

print(f'Total number of documents in src dir {len(os.listdir(src_dir))}')
# print(f'Total number of documents in raw susp dir {len(os.listdir(raw_susp_dir))}')

print(f'Total number of documents in susp dir {len(os.listdir(susp_dir))}')
