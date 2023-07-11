from flasgger import Swagger, swag_from
from flask import Flask, request
from flask.views import MethodView
import mysql.connector
import match

app = Flask(__name__)
swagger = Swagger(app)

cnx = mysql.connector.connect(
    user='root',  # MySQL username CHANEG TO 'admin1' FOR DEPLOYMENT 
    password='mixnmatchmysql',  # MySQL password
    host='localhost',  # IP address or hostname
    database='mixnmatch'  # MySQL database
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

class UserAPI(MethodView):

    @swag_from('openapi.yml')
    def get(self, user_id):
        if user_id is None:
            # return a list of users
            pass
        else:
            # expose a single user
            pass
    
    @app.route('/signup', methods=['POST'])
    @swag_from('openapi.yml')
    def post():
        # create a new user
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # check if email has been registered
        email_query = "SELECT COUNT(*) FROM user WHERE email = '" + email + "'"
        cursor.execute(email_query)
        result = cursor.fetchone()
        if (result[0] != 0) :
            return 'This email is already registered, try another one!'

         # Inserting the new user into the database
        insert_query = "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)"
        user_data = (email, username, password)
        cursor.execute(insert_query, user_data)
        cnx.commit()

        return 'User registered successfully!'

    @app.route('/update-user/<int:user_id>', methods=['PUT'])
    @swag_from('openapi.yml')
    def put(self, user_id):
        # update a single user
        pass

    @swag_from('openapi.yml')
    def delete(self, user_id):
        # delete a single user
        pass


if __name__ == '__main__':
    app.run()