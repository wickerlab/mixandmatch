from asyncio.windows_events import NULL
from types import MethodType
from flasgger import Swagger, swag_from
from flask import Flask, request, session, jsonify
from flask.views import MethodView
import mysql.connector
import match
import os

app = Flask(__name__)
swagger = Swagger(app)

app.secret_key = os.urandom(24) # temp authentication key


## change when deploy use admin1
cnx = mysql.connector.connect(
    user='root',  # MySQL username CHANEG TO 'admin1' FOR DEPLOYMENT 
    password='mixnmatchmysql',  # MySQL password
    host='localhost',  # IP address or hostname
    database='mixnmatch'  # MySQL database
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

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
    def create_user():
        # create a new user
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # check if email has been registered
        email_query = "SELECT COUNT(*) FROM user WHERE email = '" + email + "'"
        cursor.execute(email_query)
        result = cursor.fetchone()
        if (result[0] != 0) :
            return jsonify({'message': 'This email is already registered, try another one!'}), 400

         # Inserting the new user into the database
        insert_query = "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)"
        user_data = (email, username, password)
        cursor.execute(insert_query, user_data)
        cnx.commit()

        return jsonify({'message': 'User registered successfully!'}), 201
    
    @app.route('/onboarding/<int:user_id>', methods=['PUT'])
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
        query_age = 'INSERT INTO user_history_age (user_id) VALUES %s'
        query_attractiveness = 'INSERT INTO user_history_attractiveness (user_id) VALUES %s'
        query_education = 'INSERT INTO user_history_education (user_id) VALUES %s'
        query_gender = 'INSERT INTO user_history_gender (user_id) VALUES %s'
        query_salary = 'INSERT INTO user_history_salary (user_id) VALUES %s'
        query_profile = 'INSERT INTO user_profile (user_id) VALUES %s'
        cursor.execute(query_age, user_data_2)
        cursor.execute(query_attractiveness, user_data_2)
        cursor.execute(query_education, user_data_2)
        cursor.execute(query_gender, user_data_2)
        cursor.execute(query_salary, user_data_2)
        cursor.execute(query_profile, user_data_2)
        cnx.commit()

        return jsonify({'message': 'User attributes updated successfully!'}), 200
    
    @app.route('/login', methods=['POST'])
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
            session['email'] = email
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
        
    @app.route('/logout', methods=['GET'])
    def logout():
        # Clear the session to log out the user
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/update-user/<int:user_id>', methods=['PUT'])
    @swag_from('openapi.yml')
    def put(self, user_id):
        # update a single user
        pass

    @swag_from('openapi.yml')
    def delete(self, user_id):
        # delete a single user
        pass


class MatchAPI(MethodView) :
    ## incorporate the match algorithm later
    ''' UPDATES A MATCH PAIR AFTER A SWIPE '''
    @app.route('/match/<int:other_user_id>', methods=['POST'])
    @login_required
    def match_user(other_user_id):
        # Get the currently authenticated user's ID from the session
        match_decision = request.form.get('match_decision')
        user_id = session['user_id']
        match_bool = 0

        # match decision boolean
        if (match_decision == 'accept'):
            match_bool = 1

        # Perform the matching operation in the database
        # Check if the match exists between user1_id and user2_id
        select_query = "SELECT COUNT(*) FROM match WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)"
        match_data = (user_id, other_user_id, other_user_id, user_id)
        cursor.execute(select_query, match_data)
        match_count = cursor.fetchone()[0]

        if match_count == 0:
            # If the match does not exist, create a new match entry
            insert_query = "INSERT INTO match (user1_id, user2_id, user1_match, updated_time) VALUES (%s, %s, %s, NOW())"
            cursor.execute(insert_query, match_data, match_bool)
            cnx.commit()

            # TODO: CODE TO UPDATE PREFERENCE CONNECT TO RECOMMENDER.PY TO UPDATE DATABASE USER PROFILE
            
        else:
            # check match time
            update_query = "UPDATE match SET updated_time = NOW(), user1_match = %s WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)"
            match_data = (match_bool, user_id, other_user_id, other_user_id, user_id)
            cursor.execute(update_query, match_data)
            cnx.commit()

            # TODO: CODE TO UPDATE PREFERENCE CONNECT TO RECOMMENDER.PY TO UPDATE DATABASE USER PROFILE


        # Example: Updating a 'matches' table with the user IDs
        insert_query = "INSERT INTO matches (user1_id, user2_id) VALUES (%s, %s)"
        match_data = (user_id, other_user_id)
        cursor.execute(insert_query, match_data)
        cnx.commit()

        return jsonify({'message': f'Successfully updated match history with {other_user_id}'})
    
    ''' RETRIEVE 15 RANDOM USERS RANKED VIA '''
    # deploy this to compare with control

    ''' RETRIEVE 15 RANDOM USERS RANKED VIA '''
    # deploy this one as the control
    # TODO: ORDER THE LIST USING RECOMMENDER
    @app.route('/match', methods=['GET'])
    @login_required
    def recommend_users():
        # Query the database to get 15 random users
        query = "SELECT * FROM user ORDER BY RAND() LIMIT 15"
        cursor.execute(query)
        users = cursor.fetchall()

        # Format the user data as needed
        recommended_users = []
        for user in users:
            id, email, username, password, attr_age, attr_gender, attr_career, attr_education = user
            recommended_users.append({'username': username, 'attr_age': attr_age, 'attr_gender': attr_gender,
                                    'attr_career': attr_career, 'attr_education': attr_education})
            
        # TODO: connect to recommender

        return jsonify({'recommended_users': recommended_users})


if __name__ == '__main__':
    app.run()