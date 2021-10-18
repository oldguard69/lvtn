import datetime
from time import sleep
import os

from dotenv import load_dotenv, find_dotenv
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from util.file_manager import file_manager
from controllers.helpers import (
    get_response_for_request_file_sentences, return_response, allowed_file
)
from controllers.authentication import (login_controller, register_controller)

load_dotenv(find_dotenv())
SUSP_CORPUS_DIR = './corpus/susp'
SRC_CORPUS_DIR = './corpus/src'
PRODUCTION_SUSP_DIR = './corpus/production_susp'
PRODUCTION_SUSP_STATS_DIR = './corpus/production_susp_stats'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PRODUCTION_SUSP_DIR
app.secret_key = os.getenv('secret_key')

app.config["JWT_TOKEN_LOCATION"] = ["headers"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False

# Change this in your code!
app.config["JWT_SECRET_KEY"] = os.getenv('secret_key')
jwt = JWTManager(app)


@app.route("/register", methods=["POST"])
def register():
    return register_controller(request)


@app.route("/login", methods=["POST"])
def login():
    return login_controller(request)


@app.route("/only_headers")
@jwt_required(locations=["headers"])
def only_headers():
    return jsonify(foo="baz")



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

if __name__ == '__main__':
    app.run(debug=True)