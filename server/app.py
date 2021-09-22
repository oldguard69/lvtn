import os
from flask import Flask, jsonify

from core.file_manager import file_manager
from functions.helpers import get_response_for_request_file_sentences


susp_corpus_dir = './corpus/susp'
src_corpus_dir = './corpus/src'


app = Flask(__name__)



@app.route('/source-doc/<filename>')
def source_file_senteces(filename):
    return get_response_for_request_file_sentences(src_corpus_dir, filename)


@app.route('/suspicious-doc/<filename>')
def suspicious_file_sentences(filename):
    return get_response_for_request_file_sentences(susp_corpus_dir, filename)


@app.route("/suspicious-stat/<filename>")
def main(filename):
    stat = file_manager.read_json(os.path.join(susp_corpus_dir, filename))
    response = jsonify(stat)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



