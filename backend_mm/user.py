from flasgger import swag_from
from flask.views import MethodView


class UserAPI(MethodView):

    @swag_from('openapi.yml')
    def get(self, user_id):
        if user_id is None:
            # return a list of users
            pass
        else:
            # expose a single user
            pass

    @swag_from('openapi.yml')
    def post(self):
        # create a new user
        pass

    @swag_from('openapi.yml')
    def put(self, user_id):
        # update a single user
        pass

    @swag_from('openapi.yml')
    def delete(self, user_id):
        # delete a single user
        pass
