import os
from flask import Flask, jsonify
from core.file_manager import file_manager

corpus_dir = './corpus'


app = Flask(__name__)

# TODO: handle upload file and save to corpus/susp
# create embedding and match with all row in src


@app.route("/")
def main():
    stat = file_manager.read_json(os.path.join(corpus_dir, 'susp', 'susp_2.json'))
    return jsonify(stat)

