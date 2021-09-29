from os.path import join as osjoin


root_dir = '../corpus'
all_doc_dir = osjoin(root_dir, 'all_doc')

src_dir = osjoin(root_dir, 'src')
raw_susp_dir = osjoin(root_dir, 'raw_susp')
susp_dir = osjoin(root_dir, 'susp')

susp_stats_dir = osjoin(root_dir, 'susp_stats')

src_embeddings_dir = osjoin(root_dir, 'embeddings', 'src')
susp_embeddings_dir = osjoin(root_dir, 'embeddings', 'susp')
susp_embeddings_for_classification = osjoin(root_dir, 'embeddings', 'susp_for_classification')
