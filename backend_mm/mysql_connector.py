# Importing module
import mysql.connector
 
# Creating connection object
mydb = mysql.connector.MySQLConnection(
    host = "130.216.216.139",
    user = "mixnmatch",
    password = "mixnmatch"
)
 
# Printing the connection object
print('DATABASE')
print(mydb)