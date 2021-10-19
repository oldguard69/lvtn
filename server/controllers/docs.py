import os
from os.path import join as osjoin

from flask import jsonify

from controllers.model import get_a_suspicious_docs, get_suspicious_docs
from util.file_manager import file_manager

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