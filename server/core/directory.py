from os.path import join as osjoin

paper_root_dir = 'paper'
stdj_dir = osjoin(paper_root_dir, 'stdj')
ctu_dir = osjoin(paper_root_dir, 'ctu')


stats_about_file_dir = osjoin('..', 'stats_about_files')
root_dir = osjoin('..', 'corpus')

# store all documents
all_doc_dir = osjoin(root_dir, 'all_doc')

# store source documents
src_dir = osjoin(root_dir, 'src')
# store raw suspicious documents
raw_susp_dir = osjoin(root_dir, 'raw_susp')
# store suspicious documents after making plagiarism docs
susp_dir = osjoin(root_dir, 'susp')

# store plagiarism paragraph location in suspicious docs
susp_stats_dir = osjoin(root_dir, 'susp_stats')
predict_susp_stats_dir = osjoin(root_dir, 'predicted_susp_stats')

# store embedding of documents, in pickle format
embeddings_dir = 'embeddings'
src_embeddings_dir = osjoin(embeddings_dir, 'src')
susp_embeddings_dir = osjoin(embeddings_dir, 'susp')
susp_embeddings_for_classification = osjoin(
    embeddings_dir, 'susp_for_classification'
)

train_classifier_dir = 'train_classifier'
csv_dir = osjoin(train_classifier_dir, 'csv')
parquet_train_classifier_dir = osjoin(train_classifier_dir, 'parquet')
train_classifier_log_file = osjoin('log', 'train_classification_model.log')

find_plagiarism_paragraph_dir = 'find_plagiarism_paragarph'
plg_dataframe_dir = osjoin(find_plagiarism_paragraph_dir, 'plg_dataframe')
predited_stats_dir = osjoin(find_plagiarism_paragraph_dir, 'predicted_stats')
find_plg_log_file = osjoin('log', 'find_plagiarism_paragraph.log')

production_susp_dir = osjoin(root_dir, 'production_susp')
production_susp_stats_dir = osjoin(root_dir, 'production_susp_stats')
