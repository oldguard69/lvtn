import os
from flask import jsonify
from core.file_manager import file_manager


def get_response_for_request_file_sentences(corpus_dir, filename):
    sentences = file_manager.read_line_by_line(
        os.path.join(corpus_dir, filename)
        )
    response = jsonify(sentences=sentences)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response