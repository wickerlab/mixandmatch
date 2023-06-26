from flask import Flask, jsonify
from flasgger import Swagger
from user import UserAPI
from match import MatchAPI

app = Flask(__name__)
swagger = Swagger(app, template_file='openapi.yml')


@app.route('/')
def index():
    return jsonify(message='Welcome to the Dating App API!')


user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET', ])
app.add_url_rule('/users/', view_func=user_view, methods=['POST', ])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])

match_view = MatchAPI.as_view('match_api')
app.add_url_rule('/matches/', defaults={'match_id': None},
                 view_func=match_view, methods=['GET', ])
app.add_url_rule('/matches/', view_func=match_view, methods=['POST', ])
app.add_url_rule('/matches/<int:match_id>', view_func=match_view,
                 methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
