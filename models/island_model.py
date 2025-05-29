import mysql.connector
from config import Config

class IslandModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def get_island_with_provinces(self):
        self.cursor.execute("""
            SELECT island.id as island_id, island.name as island_name,
                   province.id as province_id, province.name as province_name
            FROM island
            LEFT JOIN province ON province.island_id = island.id
            ORDER BY island.id, province.id;
        """)
        data = self.cursor.fetchall()
        result = {}
        for row in data:
            island_id = row['island_id']
            if island_id not in result:
                result[island_id] = {
                    'id': island_id,
                    'name': row['island_name'],
                    'provinces': []
                }
            if row['province_id']:
                result[island_id]['provinces'].append({
                    'id': row['province_id'],
                    'name': row['province_name']
                })
        return list(result.values())

    def close(self):
        self.cursor.close()
        self.conn.close()
