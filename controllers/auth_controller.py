from flask import current_app
from extensions.bcrypt import bcrypt
from models.user_model import UserModel
from utils.jwt_helper import JWTHelper
import datetime


class AuthController:
    def register(self, name, email, password, kelas_id):
        user_model = UserModel()
        if user_model.find_by_email(email):
            user_model.close()
            return {'message': 'Email sudah digunakan'}, 400

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user_model.create_user(name, email, hashed, kelas_id)
        user_model.close()
        return {'message': 'Registrasi berhasil'}, 201

    def login(self, email, password):
        user_model = UserModel()
        user = user_model.find_by_email(email)

        if not user or not bcrypt.check_password_hash(user['password'], password):
            user_model.close()
            return {'message': 'Email atau password salah'}, 401

        token = JWTHelper.encode_token({
            'sub': user['id'],
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config['SECRET_KEY'])

        user_model.close()
        return {'token': token}, 200
