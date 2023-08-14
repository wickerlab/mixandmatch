from flask import Flask, jsonify
from flasgger import Swagger
from user import UserAPI
from match import MatchAPI
import os
from flask_cors import CORS

app = Flask(__name__)
swagger = Swagger(app, template_file='openapi.yml')
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = os.urandom(24)  # temp authentication key


@app.route('/')
def index():
    return jsonify(message='Welcome to the Dating App API!')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return jsonify({'message': 'Login required'}), 401

        # Additional validation can be performed if required, such as checking if the user exists in the database

        return f(*args, **kwargs)

    return decorated_function


# UserAPI
app.add_url_rule('/users/<int:user_id>', view_func=UserAPI.get_user, methods=['GET'])
app.add_url_rule('/users/<int:user_id>', view_func=UserAPI.update_user, methods=['PUT'])
app.add_url_rule('/login', view_func=UserAPI.login, methods=['POST'])
app.add_url_rule('/logout', view_func=UserAPI.logout, methods=['GET'])
app.add_url_rule('/signup', view_func=UserAPI.create_user, methods=['POST'])
app.add_url_rule('/onboarding/<int:user_id>', view_func=UserAPI.onboard, methods=['PUT'])
app.add_url_rule('/chat', view_func=UserAPI.get_chat, methods=['GET'])

# MatchAPI
app.add_url_rule('/matches/<int:other_user_id>', view_func=MatchAPI.match_user, methods=['POST'])
app.add_url_rule('/matches', view_func=MatchAPI.recommend_users, methods=['GET'])


@app.after_request
def apply_headers(response):
    return add_headers(response)


def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # TODO: change this to only allow your frontend
    response.headers['Access-Control-Allow-Origin'] = '*'
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
