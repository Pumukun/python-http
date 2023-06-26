import sqlite3

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
        if username == '':
            raise TypeError('username empty')
        if password == '':
            raise TypeError('password empty')

        self.cursor.execute(
            '''
                SELECT COALESCE(MAX(User_ID) + 1, 1)
                FROM Users
            '''
        )

        user_id = self.cursor.fetchone()[0]

        self.cursor.execute(
        '''
            INSERT INTO Users(User_ID, User_Name, User_Password)
            Values(?, ?, ?)
        ''', (user_id, username, password)
        )

        self.connection.commit()
        
