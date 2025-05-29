from flask import Flask, redirect, send_from_directory  # ← tambahkan redirect
from flask_restx import Api
from routes.auth import auth_ns
from extensions.bcrypt import bcrypt
from routes.kelas import kelas_ns
from routes.soal import soal_ns
from flask_jwt_extended import JWTManager  # ← Tambahkan ini
from routes.dashboard import dashboard_bp
from config import Config
from routes.island import island_ns
import os


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config.from_object(Config)
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def home():
        return redirect('/dashboard')


    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)
    # Init extensions
    bcrypt.init_app(app)
    # gunakan yang sama dengan encode
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    JWTManager(app)  # ← Tambahkan ini

    # Konfigurasi Swagger untuk JWT Bearer
    authorizations = {
        'Bearer Token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Masukkan token JWT seperti ini: **Bearer &lt;token&gt;**'
        }
    }

    # Init API dengan Swagger + JWT
    api = Api(
        app,
        version='1.0',
        title='Kuis Nusantara API',
        description='Dokumentasi Swagger untuk Login & Register',
        doc='/docs',
        authorizations=authorizations,
        security='Bearer Token'  # Set default security
    )

    # Tambahkan namespace
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(kelas_ns, path='/api/kelas')
    api.add_namespace(island_ns, path='/api/island')
    api.add_namespace(soal_ns, path='/api/soal')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5003, debug=True)
