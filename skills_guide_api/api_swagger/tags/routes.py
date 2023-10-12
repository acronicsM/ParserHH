from flask_restx import Resource
from http import HTTPStatus

from .api_functions import all_tags, get_skill_vacancies
from .api_model import ns, request_model_skills_list, get_model_list_skills, request_model_skill_vacancies_list


@ns.route("")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class Tags(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved list.', request_model_skills_list)
    @ns.expect(get_model_list_skills)
    @ns.doc(description="Возвращает список навыков")
    def get(self):
        """ Список навыков"""
        kwargs = get_model_list_skills.parse_args()

        return all_tags(**kwargs)


@ns.route("/<int:tags_id>")
@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class TagsItem(Resource):
    @ns.response(int(HTTPStatus.OK), 'Retrieved item.', request_model_skill_vacancies_list)
    @ns.doc(description="Возвращает данные навыка")
    def get(self, tags_id):
        """ Детальные данные навыка"""
        return get_skill_vacancies(tags_id)
