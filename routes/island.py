from flask_restx import Namespace, Resource
from models.island_model import IslandModel

island_ns = Namespace('Island', description='Pulau dan Provinsi')

@island_ns.route('/with-provinces')
class IslandWithProvinces(Resource):
    def get(self):
        model = IslandModel()
        data = model.get_island_with_provinces()
        model.close()
        return data
