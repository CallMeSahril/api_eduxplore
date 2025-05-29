import mysql.connector
from config import Config


class SoalModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def get_random_soal_by_kelas(self, kelas_id):
        self.cursor.execute("""
            SELECT * FROM soal
            WHERE kelas_id = %s
            ORDER BY RAND() LIMIT 1
        """, (kelas_id,))
        return self.cursor.fetchone()

    def create_soal(self, pertanyaan, gambar_path, pilihan_a, pilihan_b, pilihan_c,
                    pilihan_d, jawaban_benar, kelas_id, province_id):
        query = """
            INSERT INTO soal
            (pertanyaan, gambar, pilihan_a, pilihan_b, pilihan_c,
             pilihan_d, jawaban_benar, kelas_id, province_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            pertanyaan, gambar_path, pilihan_a, pilihan_b,
            pilihan_c, pilihan_d, jawaban_benar, kelas_id, province_id
        ))
        self.conn.commit()

    def get_all_soal(self):
        query = """
            SELECT soal.*, province.name AS province_name
            FROM soal
            JOIN province ON soal.province_id = province.id

        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_soal(self, soal_id):
        query = "DELETE FROM soal WHERE id = %s"
        self.cursor.execute(query, (soal_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.cursor.close()
        self.conn.close()
