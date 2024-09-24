from flask import Flask, jsonify, request
from flasgger import Swagger
from user import UserAPI
from match import MatchAPI
from flask import session
from flask.sessions import SecureCookieSessionInterface

import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
swagger = Swagger(app, template_file='openapi.yml')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.secret_key = os.urandom(24)  # temp authentication key
session_cookie_serializer = SecureCookieSessionInterface().get_signing_serializer(app)


@app.route('/')
def index():
    return jsonify(message='Welcome to the Dating App API!')


@cross_origin(supports_credentials=True)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return jsonify({'message': 'Login required'}), 401

        # Additional validation can be performed if required, such as checking if the user exists in the database

        return f(*args, **kwargs)

    return decorated_function


# UserAPI

user_api = UserAPI()  # Create an instance of the UserAPI class
# match_api = MatchAPI() # Create an instance of the ChatAPI


app.add_url_rule('/users/<int:user_id>', view_func=user_api.get_user, methods=['GET'])
app.add_url_rule('/users/<int:user_id>', view_func=user_api.update_user, methods=['PUT'])
app.add_url_rule('/login', view_func=user_api.login, methods=['POST'])
app.add_url_rule('/logout', view_func=user_api.logout, methods=['GET'])
app.add_url_rule('/signup', view_func=user_api.create_user, methods=['POST'])
app.add_url_rule('/onboarding/<int:user_id>', view_func=user_api.onboard, methods=['POST'])
app.add_url_rule('/chat', view_func=user_api.get_chat, methods=['GET'])
app.add_url_rule('/chat-history', view_func=user_api.get_chat_history, methods=['POST'])

# MatchAPI
app.add_url_rule('/matches/<int:other_user_id>', view_func=user_api.match_user, methods=['POST'])
app.add_url_rule('/matches', view_func=user_api.recommend_users, methods=['GET'])
app.add_url_rule('/reset-matches/<int:user_id>', view_func=user_api.remove_user_matches, methods=['POST'])

@app.after_request
def apply_headers(response):
    return add_headers(response)


def add_headers(response):
    # Check if the 'Origin' header is present in the request
    if 'Origin' in request.headers:
        # Allow requests from the specified origins
        allowed_origins = ['https://mixandmatch.wickerlab.org', 'http://localhost:5173']
        if request.headers['Origin'] in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']

    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    # response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'

    cookie = session_cookie_serializer.dumps(dict(session))
    response.headers.add('Set-Cookie', f'session={cookie}; SameSite=None; Secure')

    return response



# user_view = UserAPI.as_view('user_api')
# app.add_url_rule('/login', defaults={'user_id': None},
#                  view_func=user_view, methods=['GET', ])
# app.add_url_rule('/users/', defaults={'user_id': None},
#                  view_func=user_view, methods=['GET', ])
# app.add_url_rule('/users/', view_func=user_view, methods=['POST', ])
# app.add_url_rule('/users/<int:user_id>', view_func=user_view,
#                  methods=['GET', 'PUT', 'DELETE'])

# match_view = MatchAPI.as_view('match_api')
# app.add_url_rule('/matches/', defaults={'match_id': None},
#                  view_func=match_view, methods=['GET', ])
# app.add_url_rule('/matches/', view_func=match_view, methods=['POST', ])
# app.add_url_rule('/matches/<int:match_id>', view_func=match_view,
#                  methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
