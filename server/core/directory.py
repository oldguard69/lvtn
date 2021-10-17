from os.path import join as osjoin

stats_about_file_dir = osjoin('..', 'stats_about_files')
root_dir = osjoin('..', 'corpus')

all_doc_dir = osjoin(root_dir, 'all_doc')

src_dir = osjoin(root_dir, 'src')
raw_susp_dir = osjoin(root_dir, 'raw_susp')
susp_dir = osjoin(root_dir, 'susp')

susp_stats_dir = osjoin(root_dir, 'susp_stats')
predict_susp_stats_dir = osjoin(root_dir, 'predicted_susp_stats')

embeddings_dir = 'embeddings'
src_embeddings_dir = osjoin(embeddings_dir, 'src')
susp_embeddings_dir = osjoin(embeddings_dir, 'susp')
susp_embeddings_for_classification = osjoin(
    embeddings_dir, 'susp_for_classification'
)

production_susp_dir = osjoin(root_dir, 'production_susp')
production_susp_stats_dir = osjoin(root_dir, 'production_susp_stats')
