from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restx import Resource

from .api_functions import update
from .api_model import ns, request_model_update_dict, get_update
from ...utils.common import only_admins


@ns.route("")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error', request_model_update_dict)
class Update(Resource):
    @ns.response(int(HTTPStatus.OK), 'Vacancies updated.', request_model_update_dict)
    @jwt_required()
    @only_admins
    @ns.doc(description="Парсинг вакансий")
    def get(self):
        """ Запускает парсер обновления вакансий по списку поисковых запросов и агрегаторов вакансий """
        kwargs = get_update.parse_args()

        return update(**kwargs)
