from time import sleep
import os

from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename

from core.util.file_manager import file_manager
from core.controllers.helpers import (
    get_response_for_request_file_sentences, return_response, allowed_file
)

SUSP_CORPUS_DIR = './corpus/susp'
SRC_CORPUS_DIR = './corpus/src'
PRODUCTION_SUSP_DIR = './corpus/production_susp'
PRODUCTION_SUSP_STATS_DIR = './corpus/production_susp_stats'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PRODUCTION_SUSP_DIR
app.secret_key = "super secret key"

@app.route('/source-doc/<filename>')
def source_file_senteces(filename):
    return get_response_for_request_file_sentences(SRC_CORPUS_DIR, filename)


@app.route('/suspicious-doc/<filename>')
def suspicious_file_sentences(filename):
    return get_response_for_request_file_sentences(SUSP_CORPUS_DIR, filename)


@app.route("/suspicious-stat/<filename>")
def main(filename):
    stat = file_manager.read_json(os.path.join(SUSP_CORPUS_DIR, filename))
    response = jsonify(stat)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/upload-file', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return return_response({'msg': 'No file part'})
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return return_response({'msg': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sleep(10 * 60)
        return return_response({'msg': 'File has been uploaded'})

