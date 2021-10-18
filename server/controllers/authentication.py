from flask import  jsonify
from flask_jwt_extended import create_access_token
import datetime
from controllers.model import get_user_by_email, insert_a_user, is_user_exist

from controllers.helpers import get_hashed_password, check_password, check_post_field
from controllers.model import is_user_exist

EMAIL = 'email'
PASSWORD = 'password'
FULLNAME = 'fullname'

def register_controller(request):
    data = request.get_json()
    required_error_msg = check_post_field([EMAIL, PASSWORD, FULLNAME], data)
    if len(required_error_msg):
        return jsonify({'msg': required_error_msg})

    if is_user_exist(data[EMAIL]):
        return jsonify({'msg': ['{} has been used.'.format(data[EMAIL])]})
    
    hashed_password = get_hashed_password(data[PASSWORD])
    insert_a_user(data[EMAIL], hashed_password, data[FULLNAME])
    return jsonify({'msg': 'ok'}), 201


def login_controller(request):
    data = request.get_json()
    required_error_msg = check_post_field([EMAIL, PASSWORD], data)
    if len(required_error_msg):
        return jsonify({'msg': required_error_msg})

    user = get_user_by_email(data[EMAIL])
    if user != None:
        if check_password(data[PASSWORD], user[PASSWORD]):
            access_token = create_access_token(
                identity=user[EMAIL],
                expires_delta=datetime.timedelta(hours=300),
                additional_claims={'user_id': user['id']}
            )
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'msg': ['Wrong password.']}), 401
    else:
        return jsonify({'msg': ['User not found.']}), 404


