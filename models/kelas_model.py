import mysql.connector
from config import Config

class KelasModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all_kelas(self):
        self.cursor.execute("SELECT * FROM kelas")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
