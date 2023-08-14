from lib2to3 import refactor
import re
# from pylab import *
from enum import *
import mysql.connector

cnx = mysql.connector.connect(
    user='root',  # MySQL username CHANEG TO 'admin1' FOR DEPLOYMENT 
    password='mixnmatchmysql',  # MySQL password
    host='localhost',  # IP address or hostname
    database='mixnmatch'  # MySQL database
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

class Salary(Enum):
    BRACKET_1 = 'UNDER15'
    BRACKET_2 = '15TO30'
    BRACKET_3 = '30TO50'
    BRACKET_4 = 'OVER50'

class Age(Enum):
    BRACKET_1 = '18TO22'
    BRACKET_2 = '22TO26'
    BRACKET_3 = '26TO30'
    BRACKET_4 = 'OVER30'

class Education(Enum):
    BACHELORS = 'BACHELORS'
    MASTERS = 'MASTERS' 
    DOCTORAL = 'DOCTORAL' 
    DIPLOMA =  'DIPLOMA'

class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'

class User:
    def __init__(self, id, salary, age, gender, education):
        self.age = age
        self.id = id


        ## sort age
        self.age_category = Age.BRACKET_1
        if age > 30 :
            self.age_category = Age.BRACKET_4
        elif age <= 30 and age > 26 :
            self.age_category = Age.BRACKET_3
        elif age <= 26 and age > 22 :
            self.age_category = Age.BRACKET_2
        else :
            self.age_category = Age.BRACKET_1

        ## sort salary
        self.salary_category = Salary.BRACKET_1
        if salary == 'OVER50' :
            self.salary_category = Salary.BRACKET_4
        elif salary == '30TO50' :
            self.salary_category = Salary.BRACKET_3
        elif salary == '15TO30' :
            self.salary_category = Salary.BRACKET_2
        elif salary == 'UNDER15' :
            self.salary_category = Salary.BRACKET_1


        ## sort gender
        self.gender_category = Gender.FEMALE
        if gender == 'MALE' :
            self.gender_category = Gender.MALE
        elif gender == 'FEMALE' :
            self.gender_category = Gender.FEMALE    

        ## sort gender
        self.education_category = Education.DIPLOMA
        if education == 'BACHELORS' :
            self.education_category = Education.BACHELORS
        elif education == 'MASTERS' :
            self.education_category = Education.MASTERS
        elif education == 'DOCTORAL' :
            self.education_category = Education.DOCTORAL
        elif education == 'DIPLOMA' :
            self.education_category = Education.DIPLOMA
        self.preference = UserPreference()

    def clear_profile(self):
        self.preference = UserPreference()

class UserPreference:
    def __init__(self):
        ## [preference value, accept, reject]
        self.salary_prefs = {
            'UNDER15': [0.1, 0, 0],
            '15TO30': [0.1, 0, 0],
            '30TO50': [0.1, 0, 0],
            'OVER50': [0.1, 0, 0]
        }
        self.age_prefs = {
            '18TO22': [0.1, 0, 0],
            '22TO26': [0.1, 0, 0],
            '26TO30': [0.1, 0, 0],
            'OVER30': [0.1, 0, 0]
        }
        self.gender_prefs = {
            'MALE': [0.1, 0, 0],
            'FEMALE': [0.1, 0, 0]
        }
        self.education_prefs = {
            'BACHELORS': [0.1, 0, 0],
            'MASTERS': [0.1, 0, 0],
            'DOCTORAL': [0.1, 0, 0],
            'DIPLOMA': [0.1, 0, 0],
        }
        self.attractiveness = [0.1, 0, 0]

def get_user_attributes_by_id(user_id):
    # Query the database to get the user attributes by user_id
    query = "SELECT attr_age, attr_gender, attr_career, attr_education FROM user WHERE id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if result:
        attr_age, attr_gender, attr_career, attr_education = result
        user = User(user_id, attr_career, attr_age, attr_gender, attr_education)
    else:
        return None
    
    temp = 0 ## placeholder data

    ## Query profile
    query = "SELECT * FROM mixnmatch.user_history_age WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    fill_user_preference(user.preference.age_prefs,result)

    query = "SELECT * FROM mixnmatch.user_history_gender WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    fill_user_preference(user.preference.gender_prefs,result)

    query = "SELECT * FROM mixnmatch.user_history_salary WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    fill_user_preference(user.preference.salary_prefs,result)

    query = "SELECT * FROM mixnmatch.user_history_education WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    fill_user_preference(user.preference.education_prefs,result)

    query = "SELECT * FROM mixnmatch.user_history_attractiveness WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone() 
    i = 1
    user.preference.attractiveness[1] = result[i]
    user.preference.attractiveness[2] = result[i+1]

    update_user_preference(user)
    return user

def fill_user_preference(attribute_prefs, query) :
    i = 1
    for key in attribute_prefs :
        attribute_prefs[key][1] = query[i]
        attribute_prefs[key][2] = query[i+1]
        i = i + 2

def unidirectional_preference(u1: User, u2: User):
    """ Calculates u1's preference for u2 based on u2's attributes"""
    pref = u1.preference.salary_prefs[u2.salary_category.value][0]
    + u1.preference.age_prefs[u2.age_category.value][0]
    + u1.preference.gender_prefs[u2.gender_category.value][0]
    + u1.preference.education_prefs[u2.education_category.value][0]
    + u2.preference.attractiveness[0]

    return pref

def reciprocal_preference(u1: User, u2: User):
    """ Calculates the bidirectional preference between u1 and u2"""
    
    # calculate unidirectional preferences between u1 and u2
    u1_pref = unidirectional_preference(u1, u2)
    u2_pref = unidirectional_preference(u2, u1)

    # calculate harmonic of preference values
    r_pref = 2 / ((1/u1_pref) + (1/u2_pref))

    return r_pref


def update_user_history(u1: User, u2: User, var):
    """increment user history profile"""
    """u1 is the current user and u2 is the target user"""
    ## var = 1 means u1 accepted u2
    ## var = 2 means u1 rejected u2
    u1.preference.salary_prefs[u2.salary_category.value][var] += 1
    u1.preference.age_prefs[u2.age_category.value][var] += 1
    u1.preference.gender_prefs[u2.gender_category.value][var] += 1
    u1.preference.education_prefs[u2.education_category.value][var] += 1
    u1.preference.attractiveness[var] += 1

def update_user_preference(u1: User):
    """update user profile"""
    """u1 is the current user and u2 is the target user"""
    for key in u1.preference.age_prefs :
        if ((u1.preference.age_prefs[key][1] != 0) or (u1.preference.age_prefs[key][2] != 0)) :
            u1.preference.age_prefs[key][0] = u1.preference.age_prefs[key][1] / (u1.preference.age_prefs[key][2] + u1.preference.age_prefs[key][1])
    for key in u1.preference.salary_prefs :
        if ((u1.preference.salary_prefs[key][1] != 0) or (u1.preference.salary_prefs[key][2] != 0)) :
            u1.preference.salary_prefs[key][0] = u1.preference.salary_prefs[key][1] / (u1.preference.salary_prefs[key][2] + u1.preference.salary_prefs[key][1])       
    for key in u1.preference.education_prefs :
        if ((u1.preference.education_prefs[key][1] != 0) or (u1.preference.education_prefs[key][2] != 0)) :
            u1.preference.education_prefs[key][0] = u1.preference.education_prefs[key][1] / (u1.preference.education_prefs[key][2] + u1.preference.education_prefs[key][1]) 
    for key in u1.preference.gender_prefs :
        if ((u1.preference.gender_prefs[key][1] != 0) or (u1.preference.gender_prefs[key][2] != 0)) :
            u1.preference.gender_prefs[key][0] = u1.preference.gender_prefs[key][1] / (u1.preference.gender_prefs[key][2] + u1.preference.gender_prefs[key][1])
    if ((u1.preference.attractiveness[1] != 0) or (u1.preference.attractiveness[2] != 0)) :
            u1.preference.attractiveness[0] = u1.preference.attractiveness[1] / (u1.preference.attractiveness[2] + u1.preference.attractiveness[1])     

def order_by_preference(u1: User, user_arr) :
    """input: a user and a array of unordered users recommended to the user"""
    """sorts array of users sorted by"""
    """ assumes user_arr length > 1 """

    n = len(user_arr)
 
    # For loop to traverse through all
    # element in an array
    for i in range(n):
        for j in range(0, n - i - 1): 
            # Range of the array is from 0 to n-i-1
            # Swap the elements if the element found
            #is greater than the adjacent element
            if (reciprocal_preference(u1, user_arr[j])) > (reciprocal_preference(u1, user_arr[j+1])):

                user_arr[j], user_arr[j + 1] = user_arr[j + 1], user_arr[j]
                
    user_arr.reverse()


if __name__ == '__main__' :
    generic_user = u1 = User(Salary.BRACKET_2, 35, Gender.MALE, Education.DOCTORAL)

    # dummy data 
    u1 = User(Salary.BRACKET_2, 18, Gender.MALE, Education.DIPLOMA)
    u2 = User(Salary.BRACKET_1, 20, Gender.FEMALE, Education.DOCTORAL)
    u3 = User(Salary.BRACKET_4, 22, Gender.MALE, Education.BACHELORS)
    u4 = User(Salary.BRACKET_3, 24, Gender.FEMALE, Education.MASTERS)
    u5 = User(Salary.BRACKET_2, 26, Gender.MALE, Education.DOCTORAL)
    u6 = User(Salary.BRACKET_3, 28, Gender.FEMALE, Education.BACHELORS)
    u7 = User(Salary.BRACKET_4, 30, Gender.MALE, Education.DOCTORAL)
    u8 = User(Salary.BRACKET_3, 32, Gender.FEMALE, Education.MASTERS)
    u9 = User(Salary.BRACKET_2, 34, Gender.MALE, Education.DOCTORAL)
    u10 = User(Salary.BRACKET_3, 36, Gender.FEMALE, Education.DIPLOMA)
    u11 = User(Salary.BRACKET_2, 38, Gender.MALE, Education.DOCTORAL)
    u12 = User(Salary.BRACKET_4, 40, Gender.FEMALE, Education.BACHELORS)
    u13 = User(Salary.BRACKET_3, 42, Gender.FEMALE, Education.MASTERS)
    u14 = User(Salary.BRACKET_1, 44, Gender.MALE, Education.DIPLOMA)
    u15 = User(Salary.BRACKET_1, 46, Gender.FEMALE, Education.DIPLOMA)
    u16 = User(Salary.BRACKET_3, 19, Gender.FEMALE, Education.MASTERS)
    u17 = User(Salary.BRACKET_2, 21, Gender.MALE, Education.DOCTORAL)
    u18 = User(Salary.BRACKET_2, 23, Gender.FEMALE, Education.MASTERS)
    u19 = User(Salary.BRACKET_1, 25, Gender.FEMALE, Education.DIPLOMA)
    u20 = User(Salary.BRACKET_4, 47, Gender.MALE, Education.DOCTORAL)

    update_user_history(generic_user, u1, 1)
    update_user_history(generic_user, u2, 1)
    update_user_history(generic_user, u3, 2)
    update_user_history(generic_user, u4, 1)
    update_user_history(generic_user, u5, 2)
    update_user_history(generic_user, u6, 1)
    update_user_history(generic_user, u7, 1)
    update_user_history(generic_user, u8, 2)
    update_user_history(generic_user, u9, 2)
    update_user_history(generic_user, u10, 2)
    update_user_history(generic_user, u11, 2)
    update_user_history(generic_user, u12, 1)
    update_user_history(generic_user, u13, 2)
    update_user_history(generic_user, u14, 2)
    update_user_history(generic_user, u15, 1)
    update_user_history(generic_user, u16, 2)
    update_user_history(generic_user, u17, 1)
    update_user_history(generic_user, u18, 2)
    update_user_history(generic_user, u19, 1)
    update_user_history(generic_user, u20, 2)

    update_user_preference(generic_user)

    print('---------------- GENERIC USER\'S HISTORY: ----------------')
    for key in generic_user.preference.age_prefs :
        print(key + ' ' + str(generic_user.preference.age_prefs[key][1]) + ' ' + str(generic_user.preference.age_prefs[key][2]))
    for key in generic_user.preference.salary_prefs :
        print(key + ' ' + str(generic_user.preference.salary_prefs[key][1]) + ' ' + str(generic_user.preference.salary_prefs[key][2]))       
    for key in generic_user.preference.education_prefs :
        print(key + ' ' + str(generic_user.preference.education_prefs[key][1]) + ' ' + str(generic_user.preference.education_prefs[key][2]))
    for key in generic_user.preference.gender_prefs :
        print(key + ' ' + str(generic_user.preference.gender_prefs[key][1]) + ' ' + str(generic_user.preference.gender_prefs[key][2]))

    u_arr = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18, u19, u20]

    print('---------------- GENERIC USER\'S PREFS: ----------------')
    for key in generic_user.preference.age_prefs :
        print(key + ' ' + str(generic_user.preference.age_prefs[key][0]))
    for key in generic_user.preference.salary_prefs :
        print(key + ' ' + str(generic_user.preference.salary_prefs[key][0]))       
    for key in generic_user.preference.education_prefs :
        print(key + ' ' + str(generic_user.preference.education_prefs[key][0]))
    for key in generic_user.preference.gender_prefs :
        print(key + ' ' + str(generic_user.preference.gender_prefs[key][0]))

    order_by_preference(generic_user, u_arr)

    print('---------------- ORDERED USERS (BY AGE): ----------------')
    for u in u_arr :
        print(u.age)

    print('---------------- ORDERED USER RECIPROCATION VALUES: ----------------')
    for u in u_arr :
        print(str(reciprocal_preference(generic_user, u)))