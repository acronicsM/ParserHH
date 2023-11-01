from http import HTTPStatus
from .sql_queries import all_skills_query, get_skill_query


def all_tags(page=0, per_page=10):
    count, skills_query = all_skills_query(page, per_page)

    skills_page = [{
        'id': skill.id,
        'name': skill.name,
        'vacancies': len(skill.skill_vacancies),
        'key': sum(i.key_skills for i in skill.skill_vacancies),
        'description': sum(i.description_skills for i in skill.skill_vacancies),
        'basic': sum(i.basic_skills for i in skill.skill_vacancies),
    } for skill in skills_query.all()]

    return {'found': count, 'result': skills_page}, HTTPStatus.OK


def get_skill_vacancies(skill_id):
    return {'vacancies': [i.vacancy.to_dict() for i in get_skill_query(skill_id).skill_vacancies]}, HTTPStatus.OK
