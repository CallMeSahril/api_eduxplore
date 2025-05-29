class Config:
    SECRET_KEY = "RAHASIA_JWT_KAMU"
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'eduxplore'

    # Konfigurasi Flask-JWT-Extended
    # Di config.py
    JWT_SECRET_KEY = "RAHASIA_JWT_KAMU"
    SECRET_KEY = "RAHASIA_JWT_KAMU"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
