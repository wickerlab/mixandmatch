from asyncio.windows_events import NULL
from types import MethodType
from functools import wraps
from flasgger import Swagger, swag_from
from flask import Flask, request, session, jsonify
from flask.views import MethodView
import mysql.connector
import recommender
import match
import os

app = Flask(__name__)
swagger = Swagger(app)

# app.secret_key = os.urandom(24) # temp authentication key


## change when deploy use admin1
cnx = mysql.connector.connect(
    user='root',  # MySQL username CHANEG TO 'admin1' FOR DEPLOYMENT 
    password='mixnmatchmysql',  # MySQL password
    host='localhost',  # IP address or hostname
    database='mixnmatch'  # MySQL database
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor(buffered=True,dictionary=True)

# checks session via email
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return jsonify({'message': 'Login required'}), 401

        # Additional validation can be performed if required, such as checking if the user exists in the database

        return f(*args, **kwargs)

    return decorated_function

class UserAPI(MethodView):
    # @app.route('/user/<int:user_id>', methods=['GET'])
    @swag_from('openapi.yml')
    def get_user(user_id):

        if user_id is None:
            # return a list of users
            query = "SELECT * FROM user"
            cursor.execute(query)
            users = cursor.fetchall()
            return jsonify({'all_users': users}), 200
        else:
            query = "SELECT * FROM user WHERE (id = " + str(user_id) + ")"
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                # expose a single user
                return jsonify({'user': user}), 200
            else:
                # user does not exist
                return jsonify({'message': 'This user does not exist!'}), 404
    
    # @app.route('/signup', methods=['POST'])
    @swag_from('openapi.yml')
    def create_user():
        # create a new user
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # check if email has been registered
        email_query = "SELECT COUNT(*) FROM user WHERE email = '" + email + "'"
        cursor.execute(email_query)
        result = cursor.fetchone()
        print(result)
        if (result['COUNT(*)'] != 0) :
            return jsonify({'message': 'This email is already registered, try another one!'}), 400

         # Inserting the new user into the database
        insert_query = "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)"
        user_data = (email, username, password)
        cursor.execute(insert_query, user_data)
        cnx.commit()

        id_query = "SELECT id FROM user WHERE email = '" + email + "'"
        cursor.execute(id_query)
        user_id = cursor.fetchone()['id']

        return jsonify({'message': f'Successfully registered user with with user_id: {user_id}'}), 201
    
    # @app.route('/onboarding/<int:user_id>', methods=['PUT'])
    @swag_from('openapi.yml')
    def onboard(user_id):
        # update a user's attributes
        age = request.form.get('age')
        gender = request.form.get('gender')
        career = request.form.get('career') # we're gonna have 4 main types prob lmao
        education = request.form.get('education')

        update_query = "UPDATE user SET attr_age = %s, attr_gender = %s, attr_career = %s, attr_education = %s WHERE id = %s"
        user_data = (age, gender, career, education, user_id)
        cursor.execute(update_query, user_data)
        cnx.commit()

        # initialize empty user profile and history
        user_data_2 = (user_id)
        query_age = 'INSERT INTO user_history_age (user_id) VALUES (%s)'
        query_attractiveness = 'INSERT INTO user_history_attractiveness (user_id) VALUES (%s)'
        query_education = 'INSERT INTO user_history_education (user_id) VALUES (%s)'
        query_gender = 'INSERT INTO user_history_gender (user_id) VALUES (%s)'
        query_salary = 'INSERT INTO user_history_salary (user_id) VALUES (%s)'
        query_profile = 'INSERT INTO user_profile (user_id) VALUES (%s)'
        cursor.execute(query_age, (user_data_2,))
        cursor.execute(query_attractiveness, (user_data_2,))
        cursor.execute(query_education, (user_data_2,))
        cursor.execute(query_gender, (user_data_2,))
        cursor.execute(query_salary, (user_data_2,))
        cursor.execute(query_profile, (user_data_2,))
        cnx.commit()

        return jsonify({'message': 'User attributes updated successfully!'}), 200
    
    # @app.route('/login', methods=['POST'])
    def login():
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the provided email and password match a user in the database
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        user_data = (email, password)
        cursor.execute(query, user_data)
        user = cursor.fetchone()

        if user:
            # Set the user's email in the session to represent a logged-in user
            id_query = "SELECT id FROM user WHERE email = %s"
            cursor.execute(id_query, (email,))
            user_id = cursor.fetchone()

            ## session stores email and id
            session['email'] = email
            session['user_id'] = user_id

            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
        
    # @app.route('/logout', methods=['GET'])
    def logout():
        # Clear the session to log out the user
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200
    
    # update a single user
    # @app.route('/update-user/<int:user_id>', methods=['PUT'])
    @swag_from('openapi.yml')
    def update_user(self, user_id):
        # update a single user
        query = "SELECT * FROM user WHERE (id = " + user_id + ")"
        cursor.execute(query)
        user = cursor.fetchone()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        new_email = request.json.get('email')
        new_username = request.json.get('username')

        if new_email:
            query = "UPDATE user SET email = %s WHERE user_id = %s"
            cursor.execute(query, (new_email, user_id))
            

        if new_username:
            query = "UPDATE user SET username = %s WHERE user_id = %s"
            cursor.execute(query, (new_username, user_id))

        cnx.commit()
        return jsonify({'message': 'User updated successfully'})

    @swag_from('openapi.yml')
    def delete(self, user_id):
        # delete a single user
        # we prob dont need
        pass  

if __name__ == '__main__':
    app.run()