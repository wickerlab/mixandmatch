import mysql.connector
import recommender
import user

cnx = mysql.connector.connect(
    user='root',  # MySQL username CHANEG TO 'admin1' FOR DEPLOYMENT 
    password='mixnmatchmysql',  # MySQL password
    host='localhost',  # IP address or hostname
    database='mixnmatch'  # MySQL database
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email


def get_user_by_id(user_id):
    # Query the database to get the user instance by user_id
    query = "SELECT id, username, email FROM user WHERE id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if result:
        user_id, username, email = result
        user = User(user_id, username, email)
        return user
    else:
        return None

# Example usage
other_user = recommender.get_user_attributes_by_id(6)

# TO UPDATE PREFERENCE CONNECT TO RECOMMENDER.PY TO UPDATE DATABASE USER PROFILE
## update user 1's preference profile & user 2's attractiveness
attribute_category_insert = user.sort_profile_update_query(other_user.age_category.value, 'reject')
age_insert_query = "UPDATE mixnmatch.user_history_age SET " + attribute_category_insert + " = " + attribute_category_insert + " + 1 WHERE user_id = 5"
print(age_insert_query)

# print('---------------- GENERIC USER\'S HISTORY: ----------------')
# for key in generic_user.preference.age_prefs :
#     print(key + ' ' + str(generic_user.preference.age_prefs[key][1]) + ' ' + str(generic_user.preference.age_prefs[key][2]))
# for key in generic_user.preference.salary_prefs :
#     print(key + ' ' + str(generic_user.preference.salary_prefs[key][1]) + ' ' + str(generic_user.preference.salary_prefs[key][2]))       
# for key in generic_user.preference.education_prefs :
#     print(key + ' ' + str(generic_user.preference.education_prefs[key][1]) + ' ' + str(generic_user.preference.education_prefs[key][2]))
# for key in generic_user.preference.gender_prefs :
#     print(key + ' ' + str(generic_user.preference.gender_prefs[key][1]) + ' ' + str(generic_user.preference.gender_prefs[key][2]))

# print('---------------- GENERIC USER\'S PREFS: ----------------')
# for key in generic_user.preference.age_prefs :
#     print(key + ' ' + str(generic_user.preference.age_prefs[key][0]))
# for key in generic_user.preference.salary_prefs :
#     print(key + ' ' + str(generic_user.preference.salary_prefs[key][0]))       
# for key in generic_user.preference.education_prefs :
#     print(key + ' ' + str(generic_user.preference.education_prefs[key][0]))
# for key in generic_user.preference.gender_prefs :
#     print(key + ' ' + str(generic_user.preference.gender_prefs[key][0]))

# Closing the cursor and database connection
cursor.close()
cnx.close()