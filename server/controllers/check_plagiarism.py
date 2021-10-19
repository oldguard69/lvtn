import os
from os.path import join as osjoin
import uuid

from flask import jsonify

from controllers.model import get_a_suspicious_docs, get_suspicious_docs
from controllers.model import insert_a_suspicious_doc
from util.find_plg_paragraph import get_dataframe_contain_plagiarised_sentences
from util.file_manager import file_manager
from util.find_plg_paragraph import find_plagiarised_paragraph
from util.file_manager import file_manager
from util.sentence_transformer import sentence_transfomer

classifier = file_manager.pickle_load('./util/model/classifier.pk')


def get_response_for_request_file_sentences(corpus_dir, filename):
    sentences = file_manager.read_line_by_line(
        os.path.join(corpus_dir, filename)
        )
    response = jsonify(sentences=sentences)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def get_suspicious_docs_controller(user_id):
    docs = get_suspicious_docs(user_id)
    return jsonify({'result': docs}), 200


def get_a_suspicious_doc_controller(doc_id, user_id):
    doc = get_a_suspicious_docs(doc_id, user_id)
    if doc:
        return jsonify({'result': doc}), 200
    else:
        return jsonify(), 404



def check_plagiarism(user_id, filename, unique_filename):
    unique_filename =  unique_filename + '.json'
    is_plg = False
    num_of_sentences = 0
    num_of_plg_sentences = 0
    num_of_plg_paragraph = 0

    #compute embedding
    susp_dir = './corpus/production_susp'
    susp_stats_dir = './corpus/production_susp_stats'
    print('compute embeddings...', end='')
    susp_embeddings = sentence_transfomer.compute_embedding_of_a_doc(susp_dir, filename, 32)
    print(f'done {len(susp_embeddings)}')
    num_of_sentences = len(susp_embeddings)


    # compare susp embeddings with src embedding, using classifier to filter out plagiarised sentences
    print('get_dataframe_contain_plagiarised_sentences...', end='')
    plg_sents_df = get_dataframe_contain_plagiarised_sentences(
        susp_embeddings, classifier
    )
    print('done')


    # from plagiarised sentences dataframe, find plagiarised paragraphs
    res = find_plagiarised_paragraph(plg_sents_df)
    if len(res):
        is_plg = True
        num_of_plg_paragraph = len(res)
        num_of_plg_sentences = get_number_of_plg_sentences(res)
    
    
    for i, j in zip(
        ['filename', 'is_plg', 'num_of_sentences', 'num_of_plg_sentences', 'unique_filename', 'num_of_plg_paragraph'],
        [filename, is_plg, num_of_sentences, num_of_plg_sentences, unique_filename, num_of_plg_paragraph]
    ):
        print(f'{i}: {j}')
    file_manager.write_json(osjoin(susp_stats_dir, unique_filename), res)
    
    # insert_a_suspicious_doc(
    #     filename, num_of_sentences, is_plg, num_of_plg_sentences, plg_stats_name, user_id
    # )

    return {} # return a source_doc_stats


def get_number_of_plg_sentences(stats):
    res_set = set()
    for s in stats:
        plg_susp_index = [i for i in range(s['susp_index'], s['susp_index']+s['paragraph_length'])]
        res_set = res_set.union(set(plg_susp_index))
    return len(res_set)