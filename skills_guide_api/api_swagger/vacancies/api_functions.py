from http import HTTPStatus
from .sql_queries import all_vacancies_query, get_vacancy_query
from ... import app


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


def get_description(vacancy_id: int):
    if vacancy := get_vacancy_query(vacancy_id):
        return {
            'description': vacancy.description,
            'key_skills': [i.skill.name for i in vacancy.skill_vacancies if i.key_skills],
            'basic_skills': [i.skill.name for i in vacancy.skill_vacancies if i.basic_skills],
        }

    for agg in app.config['AGGREGATORS'].values():
        if detail_data := agg().get_detail_vacancy(vacancy_id):
            return {
                'description': detail_data['description'],
                'key_skills': list(detail_data['key_skills']),
                'basic_skills': list(detail_data['basic_skills']),
            }

    return f'Could not get detailed job details', HTTPStatus.CONFLICT
