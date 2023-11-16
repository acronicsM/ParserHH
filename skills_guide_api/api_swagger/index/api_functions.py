from http import HTTPStatus
from .sql_queries import statistics_item_query, top_vacancies_query, top_skills_query


def index_data():
    count_vacancies, count_skills = statistics_item_query(1), statistics_item_query(2)

    if not count_vacancies:
        count_vacancies = 0
    else:
        count_vacancies = count_vacancies.value_int

    if not count_skills:
        count_skills = 0
    else:
        count_skills = count_skills.value_int

    result = {
        'count_vacancies': count_vacancies,
        'count_skills': count_skills,
        'top_vacancies': top_vacancies_query(),
        'top_skills': [{'min': i.salary_min, 'max': i.salary_max, 'name': i.name, 'id': i.id}
                       for i in top_skills_query().all()]
    }

    return result, HTTPStatus.OK
