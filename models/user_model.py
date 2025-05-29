import mysql.connector
from config import Config


class UserModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def find_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone()

    def find_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return self.cursor.fetchone()

    def create_user(self, name, email, hashed_pw, kelas_id):
        self.cursor.execute(
            "INSERT INTO users (name, email, password, kelas_id) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_pw, kelas_id)
        )
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
