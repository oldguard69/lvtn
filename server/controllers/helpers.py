import os

from flask import jsonify
import bcrypt

from util.file_manager import file_manager

ALLOWED_EXTENSIONS = {'txt', 'pdf'}


def get_response_for_request_file_sentences(corpus_dir, filename):
    sentences = file_manager.read_line_by_line(
        os.path.join(corpus_dir, filename)
        )
    response = jsonify(sentences=sentences)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def return_response(data, status_code=200):
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status_code



def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    plain_text_password = plain_text_password.encode()
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt()).decode()

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    plain_text_password = plain_text_password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(plain_text_password, hashed_password)

def check_post_field(fields, data: dict):
    messages = []
    for f in fields:
        if f not in data or data[f] == '':
            messages.append(f'{f} is required.')
    return messages