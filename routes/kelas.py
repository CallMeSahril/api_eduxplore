from flask_restx import Namespace, Resource, fields
from models.kelas_model import KelasModel

kelas_ns = Namespace('Kelas', description='Endpoint data kelas')

kelas_model = kelas_ns.model('KelasModel', {
    'id': fields.Integer(readOnly=True),
    'nama_kelas': fields.String(required=True)
})

@kelas_ns.route('/')
class KelasList(Resource):
    @kelas_ns.marshal_list_with(kelas_model)
    def get(self):
        """Menampilkan semua data kelas"""
        model = KelasModel()
        data = model.get_all_kelas()
        model.close()
        return data
