from http import HTTPStatus
from .sql_queries import statistics_item_query, top_vacancies_query, top_skills_query


def index_data():
    result = {
        'count_vacancies': statistics_item_query(1).value_int,
        'count_skills': statistics_item_query(2).value_int,
        'top_vacancies': top_vacancies_query(),
        'top_skills': [{'min': i.salary_min, 'max': i.salary_max, 'name': i.name, 'id': i.id}
                       for i in top_skills_query().all()]
    }

    return result, HTTPStatus.OK
