from flasgger import swag_from
from flask.views import MethodView


class MatchAPI(MethodView):

    @swag_from('openapi.yml')
    def get(self, user_id):
        if user_id is None:
            # return a list of matches
            pass
        else:
            # expose a single match
            pass

    @swag_from('openapi.yml')
    def post(self):
        # create a new match
        pass

    @swag_from('openapi.yml')
    def put(self, match_id):
        # update a single match
        pass

    @swag_from('openapi.yml')
    def delete(self, match_id):
        # delete a single match
        pass
