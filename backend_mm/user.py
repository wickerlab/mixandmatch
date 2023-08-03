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

app.secret_key = os.urandom(24) # temp authentication key


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
    @app.route('/user/<int:user_id>', methods=['GET'])
    @swag_from('openapi.yml')
    def get_user(self, user_id):

        if user_id is None:
            # return a list of users
            query = "SELECT * FROM user"
            cursor.execute(query)
            users = cursor.fetchall()
            jsonify({'all_users': users}), 200
        else:
            query = "SELECT * FROM user WHERE (id = " + user_id + ")"
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                # expose a single user
                jsonify({'user': user}), 200
            else:
                # user does not exist
                jsonify({'message': 'This user does not exist!'}), 404
    
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
            id_query = "SELECT id FROM user WHERE email = %s"
            cursor.execute(id_query, (email,))
            user_id = cursor.fetchone()

            ## session stores email and id
            session['email'] = email
            session['user_id'] = user_id

            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
        
    @app.route('/logout', methods=['GET'])
    def logout():
        # Clear the session to log out the user
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200
    
    # update a single user
    @app.route('/update-user/<int:user_id>', methods=['PUT'])
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


## MIGRATE TO MATCH.PY LATER
class MatchAPI(MethodView) :
    ## incorporate the match algorithm later
    ''' UPDATES A MATCH PAIR AFTER A SWIPE '''
    @app.route('/match/<int:other_user_id>', methods=['POST'])
    @login_required
    def match_user(other_user_id):
        # Get the currently authenticated user's ID from the session
        match_decision = request.form.get('match_decision')
        user_id = session['user_id']['id']

        match_bool = 0
        # match decision boolean
        if (match_decision == 'accept'):
            match_bool = 1

        # Perform the matching operation in the database
        # Check if the match exists between user1_id and user2_id
        select_query = "SELECT COUNT(*) FROM mixnmatch.match WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)"
        match_data = (user_id, other_user_id, other_user_id, user_id)
        cursor.execute(select_query, match_data)
        match_count = cursor.fetchone()['COUNT(*)']

        if match_count == 0:
            # If the match does not exist, create a new match entry
            insert_query = "INSERT INTO mixnmatch.match (user1_id, user2_id, user1_match, update_time) VALUES (%s, %s, %s, NOW())"
            match_data = (user_id, other_user_id, match_bool)

            
        else:
            # check match time
            insert_query = "UPDATE mixnmatch.match SET update_time = NOW(), user1_match = %s WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)"
            match_data = (match_bool, user_id, other_user_id, other_user_id, user_id)

        # 
        other_user = recommender.get_user_attributes_by_id(other_user_id)

        # TO UPDATE PREFERENCE CONNECT TO RECOMMENDER.PY TO UPDATE DATABASE USER PROFILE
        ## update user 1's preference profile & user 2's attractiveness
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

        return jsonify({'message': f'Successfully updated match history with user_id: {other_user_id}'})
    
    ''' RETRIEVE 15 RANDOM USERS RANKED VIA '''
    # deploy this to compare with control

    #ORDER THE LIST USING RECOMMENDER
    @app.route('/match', methods=['GET'])
    @login_required
    def recommend_users():
        # Query the database to get 15 random users
        query = "SELECT * FROM user WHERE (id != " + str(session['user_id']['id']) + ") ORDER BY RAND() LIMIT 20"
        cursor.execute(query)
        users = cursor.fetchall()

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
def sort_profile_update_query(attribute, decision) :
    query_input = ''
    if (attribute == 'UNDER15') :
        query_input = 'category1'
    elif (attribute == '15TO30') :
        query_input = 'category2'
    elif (attribute == '30TO50') :
        query_input = 'category3'
    elif (attribute == 'OVER50') :
        query_input = 'category4'
    elif (attribute == '18TO22') :
        query_input = 'category1'
    elif (attribute == '22TO26') :
        query_input = 'category2'
    elif (attribute == '26TO30') :
        query_input = 'category3'
    elif (attribute == 'OVER30') :
        query_input = 'category4'
    elif (attribute == 'BACHELORS') :
        query_input = 'bachelors'
    elif (attribute == 'MASTERS') :
        query_input = 'bachelors'    
    elif (attribute == 'DOCTORAL') :
        query_input = 'doctoral'
    elif (attribute == 'DIPLOMA') :
        query_input = 'diploma'
    elif (attribute == 'MALE') :
        query_input = 'male'
    elif (attribute == 'FEMALE') :
        query_input = 'female'
    elif (attribute == 'FEMALE') :
        query_input = 'female'
    elif (attribute == 'attractiveness') :
        query_input = 'received'
    if (decision == 'accept') :
        query_input = query_input + '_accept'
    elif (decision == 'reject') :
        query_input = query_input + '_reject'
    return query_input    

if __name__ == '__main__':
    app.run()