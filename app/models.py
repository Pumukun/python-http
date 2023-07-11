import sqlite3
import hashlib
from flask_login import UserMixin, LoginManager
from flask import flash


conn_path = '/home/pumukun/GitHub/python-http/app.db'

class Database:
    def __init__(self):
        self.connection = sqlite3.connect(conn_path, check_same_thread=False)
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

    def get_user(self, user_id):
        try:
            self.cursor.execute(
                '''
                    SELECT * 
                    FROM Users
                    WHERE User_ID = ?
                    LIMIT 1
                ''', (user_id)
            )

            result = self.cursor.fetchone()
            if not result:
                print("User not found")
                return None

            return result

        except sqlite3.Error as err:
            print("sqlite3 error: " + str(err))

        return None

class User(UserMixin):
    def __init__(self, id: int):
        conn = sqlite3.connect(conn_path)
        c = conn.cursor()

        self.id: int = id
        
        c.execute('''SELECT User_Name, User_Password FROM Users WHERE User_ID = ?''', (id, ))
        row = c.fetchone()
        self.username: str = row[0]
        self.password: str = row[1]

        conn.close()

    
