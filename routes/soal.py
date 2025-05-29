from flask_restx import Namespace, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
import os

from controllers.soal_controller import SoalController

soal_ns = Namespace('soal', description='Soal endpoint')
controller = SoalController()

# Parser untuk POST soal (form-data)
soal_form_parser = reqparse.RequestParser()
soal_form_parser.add_argument(
    'pertanyaan', type=str, required=False, help='Pertanyaan (opsional jika pakai gambar)')
soal_form_parser.add_argument('gambar', type=FileStorage, location='files',
                              required=False, help='Gambar (opsional jika ada pertanyaan teks)')
soal_form_parser.add_argument(
    'province_id', type=int, required=True, help='ID provinsi')

soal_form_parser.add_argument('pilihan_a', type=str, required=True)
soal_form_parser.add_argument('pilihan_b', type=str, required=True)
soal_form_parser.add_argument('pilihan_c', type=str, required=True)
soal_form_parser.add_argument('pilihan_d', type=str, required=True)
soal_form_parser.add_argument('jawaban_benar', type=str, required=True)
soal_form_parser.add_argument('kelas_id', type=int, required=True)


@soal_ns.route('/')
class SoalRoute(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        print(f"[DEBUG] User ID dari JWT: {user_id}")
        return controller.get_soal_for_user(user_id)

    @soal_ns.expect(soal_form_parser)
    def post(self):
        args = soal_form_parser.parse_args()
        print("[DEBUG] Form args:", args)
        gambar_file = args.get('gambar')
        return controller.create_soal(args, gambar_file)
