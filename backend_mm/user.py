# from asyncio.windows_events import NULL
import os
from types import MethodType
from functools import wraps
from flasgger import Swagger, swag_from
from flask import Flask, request, session, jsonify, send_file
from flask.views import MethodView
from flask_session import Session
import mysql.connector

from flask_cors import CORS, cross_origin
from config import ApplicationConfig
from flask.sessions import SecureCookieSessionInterface

from io import BytesIO
import recommender
import match
import os

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
server_session = Session(app)
swagger = Swagger(app, template_file='openapi.yml')
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# ## change when deploy use admin1
# cnx = mysql.connector.connect(
#     user='root',  # MySQL username CHANEG TO 'admin1' FOR DEPLOYMENT
#     password='mixnmatchmysql',  # MySQL password
#     host='localhost',  # IP address or hostname
#     database='mixnmatch'  # MySQL database
# )
#
# # Create a cursor object to execute SQL queries
# cursor = cnx.cursor(buffered=True, dictionary=True)

# Create a MySQL connection pool
dbconfig = {
    "user": 'mixnmatch',  # MySQL username (CHANGE TO 'admin1' FOR DEPLOYMENT)
    "password": 'mixnmatch',  # MySQL password
    "host": 'localhost',  # IP address or hostname
    "database": 'mixnmatch',  # MySQL database
    "pool_name": "mypool",
    "pool_size": 15  # Adjust the pool size as needed
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)

class UserAPI(MethodView):

    @staticmethod
    def get_connection():
        # Get a connection from the connection pool
        return cnxpool.get_connection()

    # checks session via email
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            print(session)
            
            if 'email' not in session:
                return jsonify({'message': 'Login required'}), 401

            # Additional validation can be performed if required, such as checking if the user exists in the database

            return f(*args, **kwargs)

        return decorated_function

    @swag_from('openapi.yml')
    @login_required
    def get_user(self, user_id):

        if user_id is None:
            query = "SELECT * FROM user"
        else:
            query = "SELECT * FROM user WHERE id = %s"
        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
                cursor.execute(query, (user_id,))
                if user_id is None:
                    users = cursor.fetchall()
                    return jsonify({'all_users': users}), 200
                else:
                    user = cursor.fetchone()
                    if user:
                        return jsonify({'user': user}), 200
                    else:
                        return jsonify({'message': 'This user does not exist!'}), 404
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

    @swag_from('openapi.yml')
    def create_user(self):

        print('signing up user')
        print(request.form)

        # create a new user
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        print(email)
        print(username)
        print(password)

        # check if email has been registered
        email_query = "SELECT COUNT(*) FROM user WHERE email = '" + email + "'"
        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
                cursor.execute(email_query)
                result = cursor.fetchone()
                print(result)
                if (result['COUNT(*)'] != 0):
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
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

    @swag_from('openapi.yml')
    def onboard(self,user_id):
        # update a user's attributes
        age = request.form.get('age')
        gender = request.form.get('gender')
        career = request.form.get('career')
        education = request.form.get('education')
        photo = request.form.get('photo')
        bio = request.form.get('bio')
        update_query = "UPDATE user SET attr_age = %s, attr_gender = %s, attr_career = %s, attr_education = %s, imageURL = %s, bio = %s WHERE id = %s"
        user_data = (age, gender, career, education, photo, bio, user_id)
        

        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
                cursor.execute(update_query, user_data)
                cnx.commit()

                print('user added')

                # initialize empty user profile and history
                user_data_2 = (user_id)
                query_age = 'INSERT INTO user_history_age (user_id) VALUES (%s)'
                query_attractiveness = 'INSERT INTO user_history_attractiveness (user_id) VALUES (%s)'
                query_education = 'INSERT INTO user_history_education (user_id) VALUES (%s)'
                query_gender = 'INSERT INTO user_history_gender (user_id) VALUES (%s)'
                query_salary = 'INSERT INTO user_history_salary (user_id) VALUES (%s)'
                query_profile = 'INSERT INTO user_profile (user_id) VALUES (%s)'
                # query_category = 'INSERT INTO user_category (user_id) VALUES (%s)'
                cursor.execute(query_age, (user_data_2,))
                cursor.execute(query_attractiveness, (user_data_2,))
                cursor.execute(query_education, (user_data_2,))
                cursor.execute(query_gender, (user_data_2,))
                cursor.execute(query_salary, (user_data_2,))
                cursor.execute(query_profile, (user_data_2,))
                # cursor.execute(query_category, (user_data_2,))
                cnx.commit()

                return jsonify({'message': 'User attributes updated successfully!'}), 200
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

    def login(self):
        email = request.form.get('email')
        password = request.form.get('password')
        # Check if the provided email and password match a user in the database
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        user_data = (email, password)

        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
                cursor.execute(query, user_data)
                user = cursor.fetchone()

                if user:
                    # Set the user's email in the session to represent a logged-in user
                    id_query = "SELECT id FROM user WHERE email = %s"
                    cursor.execute(id_query, (email,))
                    user_id = cursor.fetchone()

                    # session stores email and id
                    session['email'] = email
                    session['user_id'] = user_id

                    response = jsonify({'message': 'Logged in successfully'})

                    return response, 200
                else:
                    return jsonify({'message': 'Invalid email or password'}), 401
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

    def logout(self):
        # Clear the session to log out the user
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200

    # update a single user
    @swag_from('openapi.yml')
    def update_user(self, user_id):
        # update a single user
        query = "SELECT * FROM user WHERE (id = " + user_id + ")"

        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
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
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

    @login_required
    def delete(self, user_id):
        # delete a single user
        # we prob dont need
        pass

        # get id and username of all users that session user can chat with

    @login_required
    def get_chat(self):
        # Get the currently authenticated user's ID from the session
        user_id = session['user_id']['id']

        # Define the SQL query to retrieve chat users, usernames, photos, and unread message count
        #
        select_query = """
            SELECT DISTINCT
                CASE
                    WHEN m.user1_id = %s THEN m.user2_id
                    ELSE m.user1_id
                END AS user_id,
                u.username
            FROM
                mixnmatch.match AS m
            INNER JOIN
                mixnmatch.user AS u
            ON
                CASE
                    WHEN m.user1_id = %s THEN m.user2_id
                    ELSE m.user1_id
                END = u.id
            # LEFT JOIN
            #     mixnmatch.message AS msg
            # ON
            #     (m.user1_id = msg.sender_id AND m.user2_id = msg.receiver_id)
            #     OR (m.user1_id = msg.receiver_id AND m.user2_id = msg.sender_id)
            WHERE
                %s IN (m.user1_id, m.user2_id)
                AND m.user1_match = 1
                AND m.user2_match = 1

        """
        query_data = (user_id, user_id, user_id)

        # print(query_data)

        try:
            with self.get_connection() as cnx:

                print("connected")

                cursor = cnx.cursor(dictionary=True)
                # print(select_query)
                cursor.execute(select_query, query_data)

                print("executed")

                chat_users = cursor.fetchall()

                print(chat_users)

                # Check if there are any results
                if not chat_users:
                    return jsonify({"user_id": user_id, 'chat_users': []}), 200

                return jsonify({"user_id": user_id, 'chat_users': chat_users})
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500


    @login_required
    def get_chat_history(self):
        current_user_id = request.form.get('current_user_id')
        clicked_user_id = request.form.get('clicked_user_id')

        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)

                # Update messages to "read" status
                update_query = """
                    UPDATE message
                    SET status = 'read'
                    WHERE receiver_id = %s AND sender_id = %s AND status = 'unread'
                """

                cursor.execute(update_query, (current_user_id, clicked_user_id))
                cnx.commit()

                # Print the row count affected by the UPDATE query
                print(f"Rows affected by UPDATE: {cursor.rowcount}")

                # Select chat history
                select_query = """
                    SELECT sender_id, receiver_id, message, update_time
                    FROM message
                    WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)
                    ORDER BY update_time ASC
                """
                cursor.execute(select_query, (current_user_id, clicked_user_id, clicked_user_id, current_user_id))
                history = []

                # Process the data into a list of dictionaries
                for row in cursor.fetchall():
                    history.append({
                        'sender_id': row["sender_id"],
                        'receiver_id': row["receiver_id"],
                        'message': row["message"],
                        'update_time': row["update_time"].isoformat()
                    })

                # Return the chat history as JSON response
                return jsonify({'chat_history': history}), 200
        except Exception as e:
            # Handle exceptions appropriately (e.g., log errors)
            print("ErrorMessage", e)
            return jsonify({'message': str(e)}), 500
        
    def reset_chat_history(self, user_id):
        print(user_id)

        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)

                # Remove all message entries for the current user
                delete_query = """
                    DELETE FROM mixnmatch.message 
                    WHERE sender_id = %s or receiver_id = %s
                """
                cursor.execute(delete_query, (user_id, user_id))

                # Commit the changes
                cnx.commit()

        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

        return jsonify({'message': 'Successfully removed all chat history with current user.'})

    def remove_user_matches(self, user_id):

        print(user_id)

        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)

                # Remove all match entries for the current user
                delete_query = """
                    DELETE FROM mixnmatch.match 
                    WHERE user1_id = %s or user2_id = %s
                """
                cursor.execute(delete_query, (user_id, user_id))

                # Reset user preference profiles in the following tables:
                # - user_history_age
                # - user_history_salary
                # - user_history_gender
                # - user_history_education
                # - user_history_attractiveness

                reset_query_age = """
                    UPDATE mixnmatch.user_history_age SET 
                    category1_accept = 0000000000, category1_reject = 0000000000,
                    category2_accept = 0000000000, category2_reject = 0000000000,
                    category3_accept = 0000000000, category3_reject = 0000000000,
                    category4_accept = 0000000000, category4_reject = 0000000000
                    WHERE user_id = %s
                """
                reset_query_attractiveness = """
                    UPDATE mixnmatch.user_history_attractiveness SET 
                    received_accept = 0000000000, received_reject = 0000000000
                    WHERE user_id = %s
                """
                reset_query_education = """
                    UPDATE mixnmatch.user_history_education SET 
                    bachelors_accept = 0000000000, bachelors_reject = 0000000000,
                    masters_accept = 0000000000, masters_reject = 0000000000,
                    doctoral_accept = 0000000000, doctoral_reject = 0000000000,
                    diploma_accept = 0000000000, diploma_reject = 0000000000
                    WHERE user_id = %s
                """

                reset_query_gender = """
                    UPDATE mixnmatch.user_history_gender SET 
                    male_accept = 0000000000, male_reject = 0000000000,
                    female_accept = 0000000000, female_reject = 0000000000
                    WHERE user_id = %s
                """
                reset_query_salary = """
                    UPDATE mixnmatch.user_history_salary SET 
                    category1_accept = 0000000000, category1_reject = 0000000000,
                    category2_accept = 0000000000, category2_reject = 0000000000,
                    category3_accept = 0000000000, category3_reject = 0000000000,
                    category4_accept = 0000000000, category4_reject = 0000000000
                    WHERE user_id = %s
                """

                # Execute the reset queries
                cursor.execute(reset_query_age, (user_id,))
                cursor.execute(reset_query_salary, (user_id,))
                cursor.execute(reset_query_gender, (user_id,))
                cursor.execute(reset_query_education, (user_id,))
                cursor.execute(reset_query_attractiveness, (user_id,))

                # Commit the changes
                cnx.commit()

        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

        return jsonify({'message': 'Successfully removed all matches and reset preference profiles.'})

    # @app.route('/match/<int:other_user_id>', methods=['POST'])
    @login_required
    def match_user(self, other_user_id):

        # Get the currently authenticated user's ID from the session
        match_decision = request.form.get('match_decision')
        match_time = request.form.get('match_time')
        match_time = float(match_time)
        user_id = session['user_id']['id']

        match_bool = 0
        # match decision boolean
        if (match_decision == 'accept'):
            match_bool = 1


        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)

                # Perform the matching operation in the database
                # Check if an incomplete match exists between user1_id and user2_id
                # select_query = "SELECT COUNT(*) FROM mixnmatch.match WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)"
                select_query = "SELECT COUNT(*) FROM mixnmatch.match WHERE (user1_id = %s AND user2_id = %s ) AND (user1_match IS NULL OR user2_match IS NULL)"
                match_data = (user_id, other_user_id)
                cursor.execute(select_query, match_data)
                match_count_1 = cursor.fetchone()['COUNT(*)']
                print(match_count_1)

                select_query = "SELECT COUNT(*) FROM mixnmatch.match WHERE (user2_id = %s AND user1_id = %s ) AND (user1_match IS NULL OR user2_match IS NULL)"
                match_data = (user_id, other_user_id)
                cursor.execute(select_query, match_data)
                match_count_2 = cursor.fetchone()['COUNT(*)']
                print(match_count_2)

                ## classify the match situation
                match_class = 0  ## no partial matches
                if (match_count_1 == 1):
                    match_class = 1  ## partial match + session user is user 1
                elif (match_count_2 == 1):
                    match_class = 2  ## partial match + session user is user 2

                ## update match history
                if match_class == 0:
                    # If an incomplete match does not exist, create a new match entry
                    insert_query = "INSERT INTO mixnmatch.match (user1_id, user2_id, user1_match, user1_update_time, user1_decision_time) VALUES (%s, %s, %s, NOW(), %s)"
                    match_data = (user_id, other_user_id, match_bool, match_time)

                elif match_class == 1:
                    # If an incomplete match does exist, update match entry
                    insert_query = "UPDATE mixnmatch.match SET user1_update_time = NOW(), user1_match = %s, user1_decision_time = %s WHERE (user1_id = %s AND user2_id = %s ) AND (user1_match IS NULL OR user2_match IS NULL)"
                    match_data = (match_bool, match_time, user_id, other_user_id)

                elif match_class == 2:
                    # check match time
                    insert_query = "UPDATE mixnmatch.match SET user2_update_time = NOW(), user2_match = %s, user2_decision_time = %s WHERE (user2_id = %s AND user1_id = %s ) AND (user1_match IS NULL OR user2_match IS NULL)"
                    match_data = (match_bool, match_time, user_id, other_user_id)

                # Get other user's attributes
                try: 
                    other_user = recommender.get_user_attributes_by_id(other_user_id)
                except:
                    return jsonify({'error matching'}), 500

                # update user preference profile
                attribute_category_insert = sort_profile_update_query(other_user.age_category.value, match_decision)
                age_insert_query = "UPDATE mixnmatch.user_history_age SET " + attribute_category_insert + " = " + attribute_category_insert + " + 1 WHERE user_id = %s"
                attribute_category_insert = sort_profile_update_query(other_user.salary_category.value, match_decision)
                salary_insert_query = "UPDATE mixnmatch.user_history_salary SET " + attribute_category_insert + " = " + attribute_category_insert + " + 1 WHERE user_id = %s"
                attribute_category_insert = sort_profile_update_query(other_user.gender_category.value, match_decision)
                gender_insert_query = "UPDATE mixnmatch.user_history_gender SET " + attribute_category_insert + " = " + attribute_category_insert + " + 1 WHERE user_id = %s"
                attribute_category_insert = sort_profile_update_query(other_user.education_category.value, match_decision)
                education_insert_query = "UPDATE mixnmatch.user_history_education SET " + attribute_category_insert + " = " + attribute_category_insert + " + 1 WHERE user_id = %s"
                attribute_category_insert = sort_profile_update_query('attractiveness', match_decision)
                attractive_insert_query = "UPDATE mixnmatch.user_history_attractiveness SET " + attribute_category_insert + " = " + attribute_category_insert + " + 1 WHERE user_id = %s"

                ## only execute if no errors
                cursor.execute(insert_query, match_data)
                cursor.execute(age_insert_query, (user_id,))
                cursor.execute(salary_insert_query, (user_id,))
                cursor.execute(gender_insert_query, (user_id,))
                cursor.execute(education_insert_query, (user_id,))
                cursor.execute(attractive_insert_query, (other_user_id,))
                cnx.commit()

        # Close connection to database
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

        return jsonify({'message': f'Successfully updated match history with user_id: {other_user_id}'})

    ''' RETRIEVE 15 RANDOM USERS RANKED VIA '''

    # deploy this to compare with control

    # ORDER THE LIST USING RECOMMENDER
    @login_required
    def recommend_users(self):
        # Open Connection to database
        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
                # Query the database to get 15 random users excluding session user
                # user_id = session['user_id']['id']
                # query_category = 'SELECT category FROM mixnmatch.user_category WHERE user_id = %s'
                # cursor.execute(query_category, (user_id,))
                # category = cursor.fetchone()['category']
                # print(category)

                category = "None"

                if category == 'BOT':
                    query = "SELECT * FROM user JOIN user_category ON (user.id = user_category.user_id) WHERE (user.id != " + str(session['user_id']['id']) + ") " \
                            + "AND user.attr_age IS NOT NULL " \
                            + "AND user.attr_gender IS NOT NULL " \
                            + "AND user.attr_career IS NOT NULL " \
                            + "AND user.attr_education IS NOT NULL " \
                            + "AND user_category.category = 'HUMAN'" \
                        # + "ORDER BY RAND() LIMIT 20"
                elif category == 'HUMAN':
                    query = "SELECT * FROM user JOIN mixnmatch.user_category ON (user.id = user_category.user_id) WHERE (user.id != " + str(session['user_id']['id']) + ") " \
                            + "AND user.attr_age IS NOT NULL " \
                            + "AND user.attr_gender IS NOT NULL " \
                            + "AND user.attr_career IS NOT NULL " \
                            + "AND user.attr_education IS NOT NULL " \
                            + "AND user_category.category = 'BOT'" \
                            + "ORDER BY RAND() LIMIT 20"
                else :
                    query = "SELECT * FROM user WHERE (id != " + str(session['user_id']['id']) + ") " \
                            + "AND attr_age IS NOT NULL " \
                            + "AND attr_gender IS NOT NULL " \
                            + "AND attr_career IS NOT NULL " \
                            + "AND attr_education IS NOT NULL " \
                            + "ORDER BY RAND() LIMIT 20"
                cursor.execute(query)
                users = cursor.fetchall()

        # Close connection to database
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

        session_user = recommender.get_user_attributes_by_id(session['user_id']['id'])

        # Format the user data as needed
        recommended_users = []
        for user in users:
            recommended_users.append(recommender.get_user_attributes_by_id(user['id']))

        # call recommender function
        recommender.order_by_preference(session_user, recommended_users)

        output_user_json = []
        for user in recommended_users:
            output_user_json.append(next(item for item in users if item["id"] == user.id))

        return jsonify({'recommended_users': output_user_json})
    

def sort_profile_update_query(attribute, decision):
    query_input = ''
    if (attribute == 'UNDER15'):
        query_input = 'category1'
    elif (attribute == '15TO30'):
        query_input = 'category2'
    elif (attribute == '30TO50'):
        query_input = 'category3'
    elif (attribute == 'OVER50'):
        query_input = 'category4'
    elif (attribute == '18TO22'):
        query_input = 'category1'
    elif (attribute == '22TO26'):
        query_input = 'category2'
    elif (attribute == '26TO30'):
        query_input = 'category3'
    elif (attribute == 'OVER30'):
        query_input = 'category4'
    elif (attribute == 'BACHELORS'):
        query_input = 'bachelors'
    elif (attribute == 'MASTERS'):
        query_input = 'bachelors'
    elif (attribute == 'DOCTORAL'):
        query_input = 'doctoral'
    elif (attribute == 'DIPLOMA'):
        query_input = 'diploma'
    elif (attribute == 'MALE'):
        query_input = 'male'
    elif (attribute == 'FEMALE'):
        query_input = 'female'
    elif (attribute == 'FEMALE'):
        query_input = 'female'
    elif (attribute == 'attractiveness'):
        query_input = 'received'
    if (decision == 'accept'):
        query_input = query_input + '_accept'
    elif (decision == 'reject'):
        query_input = query_input + '_reject'
    return query_input

if __name__ == '__main__':
    app.run()
