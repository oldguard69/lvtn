import os
import uuid
from time import sleep
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from flask import Flask, flash, request, jsonify
from flask_jwt_extended.utils import get_jwt
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from controllers.check_plagiarism import check_plagiarism
from controllers.check_plagiarism import handle_pdf
from util.merge_overlapping_paragraph import merge_overlapping_paragraph
from util.file_manager import file_manager
from controllers.helpers import return_response, allowed_file
from controllers.authentication import (login_controller, register_controller)
from controllers.docs import (
    get_response_for_request_file_sentences,
    get_a_suspicious_doc_controller, 
    get_suspicious_docs_controller,
    calulate_cos_sim_controller
)


load_dotenv(find_dotenv())
SRC_CORPUS_DIR = './corpus/src'
PRODUCTION_SUSP_DIR = './corpus/production_susp'
PRODUCTION_SUSP_PDF_DIR = os.path.join(PRODUCTION_SUSP_DIR, 'pdf')
PRODUCTION_SUSP_STATS_DIR = './corpus/production_susp_stats'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PRODUCTION_SUSP_DIR
app.config['UPLOAD_PDF_FOLDER'] = PRODUCTION_SUSP_PDF_DIR
app.secret_key = os.getenv('secret_key')
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
CORS(app)

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
# app.config["JWT_COOKIE_SECURE"] = False

app.config["JWT_SECRET_KEY"] = os.getenv('secret_key')
jwt = JWTManager(app)


@app.route("/register", methods=["POST"])
def register():
    return register_controller(request)


@app.route("/login", methods=["POST"])
def login():
    return login_controller(request)


@app.route('/source-doc-sentences/<filename>')
def source_file_senteces(filename):
    return get_response_for_request_file_sentences(SRC_CORPUS_DIR, filename)


@app.route('/suspicious-doc-sentences/<filename>')
def suspicious_file_sentences(filename):
    return get_response_for_request_file_sentences(PRODUCTION_SUSP_DIR, filename)


@app.route("/suspicious-stats/<filename>")
def main(filename):
    stats = file_manager.read_json(os.path.join(PRODUCTION_SUSP_STATS_DIR, filename))
    stats = merge_overlapping_paragraph(stats)
    response = jsonify(stats)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/upload-file', methods=['POST'])
@jwt_required(locations=["headers"])
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

    
    user_id = get_jwt()['user_id']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        unique_name = filename + '_' + str(uuid.uuid4())
        
        if filename[-3:] == 'pdf':
            pdf_file = os.path.join(app.config['UPLOAD_PDF_FOLDER'], unique_name) 
            file.save(pdf_file)
            res = handle_pdf(pdf_file, user_id, filename, unique_name)
        else:   
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
            res = check_plagiarism(user_id, filename, unique_name)

        return return_response({'result': res})


@app.route('/suspicious-docs')
@jwt_required(locations=["headers"])
def get_suspicious_docs():
    return get_suspicious_docs_controller(get_jwt()['user_id'])


@app.route('/suspicious-docs/<doc_id>')
@jwt_required(locations=["headers"])
def get_a_suspicious_doc(doc_id):
    return get_a_suspicious_doc_controller(doc_id, get_jwt()['user_id'])


@app.route('/calulcate-cosine-similarity', methods=['POST'])
def calculate_cosine_sim():
    return calulate_cos_sim_controller(request)