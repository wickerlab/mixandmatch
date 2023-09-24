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
    "user": 'root',  # MySQL username (CHANGE TO 'admin1' FOR DEPLOYMENT)
    "password": 'mixnmatchmysql',  # MySQL password
    "host": 'localhost',  # IP address or hostname
    "database": 'mixnmatch',  # MySQL database
    "pool_name": "mypool",
    "pool_size": 5  # Adjust the pool size as needed
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
            if 'email' not in session:
                return jsonify({'message': 'Login required'}), 401

            # Additional validation can be performed if required, such as checking if the user exists in the database

            return f(*args, **kwargs)

        return decorated_function

    # @app.route('/user/<int:user_id>', methods=['GET'])
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

    # @app.route('/signup', methods=['POST'])
    @swag_from('openapi.yml')
    def create_user(self):
        # create a new user
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

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

    # @app.route('/onboarding/<int:user_id>', methods=['PUT'])
    @swag_from('openapi.yml')
    def onboard(self,user_id):
        # update a user's attributes
        age = request.form.get('age')
        gender = request.form.get('gender')
        career = request.form.get('career')
        education = request.form.get('education')
        photo = request.form.get('photo')

        update_query = "UPDATE user SET attr_age = %s, attr_gender = %s, attr_career = %s, attr_education = %s, photo = %s WHERE id = %s"
        user_data = (age, gender, career, education, photo, user_id)

        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
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
                query_category = 'INSERT INTO user_category (user_id) VALUES (%s)'
                cursor.execute(query_age, (user_data_2,))
                cursor.execute(query_attractiveness, (user_data_2,))
                cursor.execute(query_education, (user_data_2,))
                cursor.execute(query_gender, (user_data_2,))
                cursor.execute(query_salary, (user_data_2,))
                cursor.execute(query_profile, (user_data_2,))
                cursor.execute(query_category, (user_data_2,))
                cnx.commit()

                return jsonify({'message': 'User attributes updated successfully!'}), 200
        except mysql.connector.Error as err:
            # Handle database errors
            return jsonify({'error': str(err)}), 500

    # @app.route('/login', methods=['POST'])
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
        select_query = """
            SELECT DISTINCT
                CASE
                    WHEN m.user1_id = %s THEN m.user2_id
                    ELSE m.user1_id
                END AS user_id,
                u.username,
                u.photo,
                COUNT(CASE WHEN msg.status = 'unread' THEN 1 ELSE NULL END) AS unread_count
            FROM
                mixnmatch.match AS m
            INNER JOIN
                mixnmatch.user AS u
            ON
                CASE
                    WHEN m.user1_id = %s THEN m.user2_id
                    ELSE m.user1_id
                END = u.id
            LEFT JOIN
                mixnmatch.message AS msg
            ON
                (m.user1_id = msg.sender_id AND m.user2_id = msg.receiver_id)
                OR (m.user1_id = msg.receiver_id AND m.user2_id = msg.sender_id)
            WHERE
                (%s IN (m.user1_id, m.user2_id))
                AND (m.user1_match = 1 OR m.user2_match = 1)
            GROUP BY
                user_id, u.username, u.photo
        """
        query_data = (user_id, user_id, user_id)

        try:
            with self.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
                cursor.execute(select_query, query_data)
                chat_users = cursor.fetchall()

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

if __name__ == '__main__':
    app.run()
