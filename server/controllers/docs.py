import os
from os.path import join as osjoin

from flask import jsonify
import pandas as pd

from controllers.model import get_a_suspicious_docs, get_suspicious_docs
from controllers.check_plagiarism import classifier
from util.file_manager import file_manager
from util.text_cleaner import text_cleaner
from util.word_segmenter import word_segmenter
from util.sentence_transformer import sentence_transfomer
from util.cosine_similarity import calculate_cosine_similarity


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


def calulate_cos_sim_controller(request):
    data = request.get_json()
    sent1 = data['sent1']
    sent2 = data['sent2']
    is_perform_removal = data['perform_cleaning']

    if is_perform_removal:
        sent1 = perform_text_cleaning(sent1)
        sent2 = perform_text_cleaning(sent2)
    else:
        sent1 = no_text_cleaning(sent1)
        sent2 = no_text_cleaning(sent2)

    sent1_embs = sentence_transfomer.encode([sent1])[0]
    sent2_embs = sentence_transfomer.encode([sent2])[0]
    cos_sim = calculate_cosine_similarity(sent1_embs, sent2_embs)
    is_plg = predict(cos_sim)
    return jsonify(result={'cosine_similarity': cos_sim, 'is_plagiarism': is_plg}), 200


def perform_text_cleaning(text):
    text = text_cleaner.remove_punctuation(text_cleaner.lowercase(text))
    return word_segmenter.segment_word(text)


def no_text_cleaning(text):
    return word_segmenter.segment_word(text)

def predict(value):
    y_pred = classifier.predict(pd.DataFrame([value], columns=['cosine_similarity']))

    is_plg = False
    if y_pred[0] == 1:
        is_plg = True
    return is_plg
