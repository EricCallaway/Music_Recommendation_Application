import mysql.connector
from mysql.connector import errorcode
from utility.secret import password as p

try:
    db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=p,
    database="music_recommendation_application"
)
except mysql.connector..Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)
else:
    db.close()
