from pylab import *
from enum import *

class Salary(Enum):
    BRACKET_1 = 'UNDER50'
    BRACKET_2 = '50TO80'
    BRACKET_3 = '80TO120'
    BRACKET_4 = 'OVER120'

class Age(Enum):
    BRACKET_1 = '18TO25'
    BRACKET_2 = '25TO35'
    BRACKET_3 = '35TO45'
    BRACKET_4 = 'OVER45'

class Education(Enum):
    NONE = 'NONE'
    PRIMARY = 'PRIMARY'
    SECONDARY = 'SECONDARY' 
    UNDERGRADUATE = 'UNDERGRADUATE' 
    POSTGRADUATE =  'POSTGRADUATE'

class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'

class User:
    def __init__(self, salary, age, gender, education):
        self.age = age

        self.age_category = Age.BRACKET_4
        if age > 45 :
            self.age_category = Age.BRACKET_4
        elif age <= 45 and age > 35 :
            self.age_category = Age.BRACKET_3
        elif age <= 35 and age > 32 :
            self.age_category = Age.BRACKET_2
        else :
            self.age_category = Age.BRACKET_1

        self.salary_category = salary
        self.gender_category = gender
        self.education_category = education

        self.preference = UserPreference()

    def clear_profile(self):
        self.preference = UserPreference()

class UserPreference:
    def __init__(self):
        self.salary_prefs = {
            'UNDER50': [0.1, 0, 0],
            '50TO80': [0.1, 0, 0],
            '80TO120': [0.1, 0, 0],
            'OVER120': [0.1, 0, 0]
        }
        self.age_prefs = {
            '18TO25': [0.1, 0, 0],
            '25TO35': [0.1, 0, 0],
            '35TO45': [0.1, 0, 0],
            'OVER45': [0.1, 0, 0]
        }
        self.gender_prefs = {
            'MALE': [0.1, 0, 0],
            'FEMALE': [0.1, 0, 0]
        }
        self.education_prefs = {
            'NONE': [0.1, 0, 0],
            'PRIMARY': [0.1, 0, 0],
            'SECONDARY': [0.1, 0, 0],
            'UNDERGRADUATE': [0.1, 0, 0],
            'POSTGRADUATE': [0.1, 0, 0]
        }

def unidirectional_preference(u1: User, u2: User):
    """ Calculates u1's preference for u2 based on u2's attributes"""
    pref = u1.preference.salary_prefs[u2.salary_category.value][0]
    + u1.preference.age_prefs[u2.age_category.value][0]
    + u1.preference.gender_prefs[u2.gender_category.value][0]
    + u1.preference.education_prefs[u2.education_category.value][0]

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


if __name__ == '__main__' :
    generic_user = u1 = User(Salary.BRACKET_2, 35, Gender.MALE, Education.UNDERGRADUATE)

    # dummy data 
    u1 = User(Salary.BRACKET_2, 18, Gender.MALE, Education.POSTGRADUATE)
    u2 = User(Salary.BRACKET_1, 20, Gender.FEMALE, Education.UNDERGRADUATE)
    u3 = User(Salary.BRACKET_4, 22, Gender.MALE, Education.PRIMARY)
    u4 = User(Salary.BRACKET_3, 24, Gender.FEMALE, Education.SECONDARY)
    u5 = User(Salary.BRACKET_2, 26, Gender.MALE, Education.UNDERGRADUATE)
    u6 = User(Salary.BRACKET_3, 28, Gender.FEMALE, Education.PRIMARY)
    u7 = User(Salary.BRACKET_4, 30, Gender.MALE, Education.UNDERGRADUATE)
    u8 = User(Salary.BRACKET_3, 32, Gender.FEMALE, Education.SECONDARY)
    u9 = User(Salary.BRACKET_2, 34, Gender.MALE, Education.UNDERGRADUATE)
    u10 = User(Salary.BRACKET_3, 36, Gender.FEMALE, Education.POSTGRADUATE)
    u11 = User(Salary.BRACKET_2, 38, Gender.MALE, Education.UNDERGRADUATE)
    u12 = User(Salary.BRACKET_4, 40, Gender.FEMALE, Education.PRIMARY)
    u13 = User(Salary.BRACKET_3, 42, Gender.FEMALE, Education.SECONDARY)
    u14 = User(Salary.BRACKET_1, 44, Gender.MALE, Education.POSTGRADUATE)
    u15 = User(Salary.BRACKET_1, 46, Gender.FEMALE, Education.POSTGRADUATE)
    u16 = User(Salary.BRACKET_3, 19, Gender.FEMALE, Education.SECONDARY)
    u17 = User(Salary.BRACKET_2, 21, Gender.MALE, Education.UNDERGRADUATE)
    u18 = User(Salary.BRACKET_2, 23, Gender.FEMALE, Education.SECONDARY)
    u19 = User(Salary.BRACKET_1, 25, Gender.FEMALE, Education.POSTGRADUATE)
    u20 = User(Salary.BRACKET_4, 47, Gender.MALE, Education.UNDERGRADUATE)

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
