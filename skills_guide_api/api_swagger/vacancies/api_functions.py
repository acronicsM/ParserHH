from http import HTTPStatus
from .sql_queries import all_vacancies_query, get_vacancy_query


def get_all_vacancies(page=0, per_page=10, tag_id=None, query_id=None, new_vacancies=False):
    count, result = all_vacancies_query(page=page,
                                        per_page=per_page,
                                        tag_id=tag_id,
                                        query_id=query_id,
                                        new_vacancies=new_vacancies)

    result = [vacancy.to_dict() for vacancy in result.all()]

    return {'found': count, 'result': result}, HTTPStatus.OK


def get_vacancy(vacancy_id: int):
    return get_vacancy_query(vacancy_id).to_dict_detail(), HTTPStatus.OK


def get_vacancy_skills(vacancy_id):
    vacancy = get_vacancy_query(vacancy_id)
    if not vacancy:
        return []
    return {'skills': [skill.to_dict() for skill in vacancy.skill_vacancies]}
