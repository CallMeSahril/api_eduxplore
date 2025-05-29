from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from extensions.bcrypt import bcrypt
from models.user_model import UserModel
from controllers.auth_controller import AuthController


auth_ns = Namespace('Auth', description='Auth Endpoints')  # ← HARUS ada ini
controller = AuthController()

register_model = auth_ns.model('Register', {
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'kelas_id': fields.Integer(required=True, description='ID kelas dari tabel kelas (1-6)')
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = auth_ns.payload
        return controller.register(data['name'], data['email'], data['password'], data['kelas_id'])


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = auth_ns.payload
        user_model = UserModel()
        user = user_model.find_by_email(data['email'])

        if not user or not bcrypt.check_password_hash(user['password'], data['password']):
            user_model.close()
            return {'message': 'Email atau password salah'}, 401

        access_token = create_access_token(
            identity=str(user['id']),  # <- PENTING: jadikan string
            additional_claims={
                'user_id': user['id'],
                'kelas_id': user['kelas_id']
            }
        )

        user_model.close()
        return {'token': access_token}, 200
