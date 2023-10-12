from flask_restx import Resource
from http import HTTPStatus
from .api_functions import get_images
from .api_model import ns


@ns.route("")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class Images(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved data.')
    @ns.doc(description="Изображения")
    def get(self):
        """ Изображения анализа данных """

        return get_images()
