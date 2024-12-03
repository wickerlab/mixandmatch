# from asyncio.windows_events import NULL
from types import MethodType
from functools import wraps
from flasgger import Swagger, swag_from
from flask import Flask, request, session, jsonify
from flask.views import MethodView
import mysql.connector
from flask_session import Session
from flask_cors import CORS, cross_origin

from config import ApplicationConfig

import recommender
import match
import os

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
server_session = Session(app)
swagger = Swagger(app, template_file='openapi.yml')
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

app.secret_key = os.urandom(24)  # temp authentication key

## change when deploy use admin1
## Opens connection to database
# def open_connection() :
#     cnx = mysql.connector.connect(
#         user='root',  # MySQL username CHANEG TO 'admin1' FOR DEPLOYMENT 
#         password='mixnmatchmysql',  # MySQL password
#         host='localhost',  # IP address or hostname
#         database='mixnmatch'  # MySQL database
#     )

#     # Create a cursor object to execute SQL queries
#     return cnx
# def open_cursor(cnx, cursor) :
#     # Create a cursor object to execute SQL queries
#     cursor = cnx.cursor(buffered=True, dictionary=True)
#     return cursor
# def close_connection (cnx, cursor) :
#     cnx.close()
#     cursor.close()


# Create a MySQL connection pool
dbconfig = {
    "user": 'mixnmatch',  # MySQL username (CHANGE TO 'admin1' FOR DEPLOYMENT)
    "password": 'mixnmatch',  # MySQL password
    "host": 'localhost',  # IP address or hostname
    "database": 'mixnmatch',  # MySQL database
    "pool_name": "mypool",
    "pool_size": 5  # Adjust the pool size as needed
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)


# checks session via email
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return jsonify({'message': 'Login required'}), 401

        # Additional validation can be performed if required, such as checking if the user exists in the database

        return f(*args, **kwargs)

    return decorated_function


## MIGRATE TO MATCH.PY LATER
class MatchAPI(MethodView):
    ## incorporate the match algorithm later
    ''' UPDATES A MATCH PAIR AFTER A SWIPE '''

    @staticmethod
    def get_connection():
        # Get a connection from the connection pool
        return cnxpool.get_connection()

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
                    # If an incomplete match does not exist, create a new match entry
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
                user_id = session['user_id']['id']
                query_category = 'SELECT category FROM mixnmatch.user_category WHERE user_id = %s'
                cursor.execute(query_category, (user_id,))
                category = cursor.fetchone()['category']
                print(category)

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


## maybe refactor this i gave up
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
