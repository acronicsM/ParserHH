from http import HTTPStatus

from skills_guide_api.utils.common import create_successful_response
from .sql_queries import max_salary_query, min_salary_query, new_query, delete_query, vacancies_query


def queries_dict(query_id=None):
    max_salary = max_salary_query(query_id).all()
    min_salary_from, min_salary_to = map(lambda x: x.all(), min_salary_query(query_id))

    response = {i[3]: {'id': i[3],
                       'name': i[4],
                       'count': i[2],
                       'max': max(i[0] if i[0] else 0, i[1] if i[1] else 0)}
                for i in max_salary}

    for i in min_salary_from:
        response[i[1]]['min'] = i[0] if i[0] else 0

    for i in min_salary_to:
        response[i[1]]['min'] = min(response[i[1]]['min'], (i[0] if i[0] else 0))

    return response


def retrieve_queries_list():
    return {'queries': [i for i in queries_dict().values()]}, HTTPStatus.OK


def create_query(parameters: dict):
    new_query_id = new_query(parameters['name'])

    return queries_dict(new_query_id)[new_query_id], HTTPStatus.CREATED


def remove_query(parameters: dict):
    delete_query(parameters['id'])

    return create_successful_response(
        status_code=HTTPStatus.OK,
        message='successfully removed',
    )


def get_query(query_id):
    return [i.to_dict() for i in vacancies_query(query_id).all()], HTTPStatus.OK
