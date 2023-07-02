import sqlite3
import hashlib
from flask_login import UserMixin, LoginManager

conn = sqlite3.connect('/home/pumukun/GitHub/python-http/app.db')

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('/home/pumukun/GitHub/python-http/app.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS Users(
                User_ID INTEGER PRIMARY KEY,
                User_Name VARCHAR,
                User_Password VARCHAR
            )
        '''
        )

    def add_user(self, username: str, password: str):
        self.cursor.execute(
            '''
                SELECT COALESCE(MAX(User_ID) + 1, 1)
                FROM Users
            '''
        )

        password = hashlib.md5(password.encode()).hexdigest()

        user_id = self.cursor.fetchone()[0]

        self.cursor.execute(
        '''
            INSERT INTO Users(User_ID, User_Name, User_Password)
            Values(?, ?, ?)
        ''', (user_id, username, password)
        )

        self.connection.commit()
    
    def sign_in(self, username: str, password: str):
        password = hashlib.md5(password.encode()).hexdigest()

        self.cursor.execute(
            '''
                SELECT User_ID
                FROM Users
                WHERE User_Name = ? AND User_Password = ?
            ''', (username, password)
        )

        try:
            tmp_user_ID = self.cursor.fetchone()[0]
            return tmp_user_ID
        except:
            return -1

    def delete_user(self, user_ID: int):
        self.cursor.execute(
            '''
                DELETE FROM Users
                WHERE User_ID = ?
            ''', (user_ID)
        )

        self.connection.commit()

class User(UserMixin):
    id = 0 

