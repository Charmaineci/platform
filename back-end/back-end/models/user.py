from datetime import datetime
import pymysql
from config import MYSQL_CONFIG

class User:
    def __init__(self):
        self.conn = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.create_table()

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def register(self, username, password, email):
        try:
            sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (username, password, email))
            self.conn.commit()
            return True
        except pymysql.Error as e:
            print(f"Error: {e}")
            return False

    def login(self, username, password):
        try:
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(sql, (username, password))
            user = self.cursor.fetchone()
            return user
        except pymysql.Error as e:
            print(f"Error: {e}")
            return None

    def get_user_by_username(self, username):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            return self.cursor.fetchone()
        except pymysql.Error as e:
            print(f"Error: {e}")
            return None

    def get_user_by_id(self, user_id):
        try:
            sql = "SELECT * FROM users WHERE id = %s"
            self.cursor.execute(sql, (user_id,))
            return self.cursor.fetchone()
        except pymysql.Error as e:
            print(f"Error: {e}")
            return None

    def __del__(self):
        self.cursor.close()
        self.conn.close() 