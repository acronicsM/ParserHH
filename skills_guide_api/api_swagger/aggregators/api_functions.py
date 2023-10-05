from http import HTTPStatus

from skills_guide_api.utils.common import _create_successful_response
from .sql_queries import aggregators_query, new_aggregator, delete_aggregator


def retrieve_aggregators_list():
    return {'aggregators': [{'id': str(i)} for i in aggregators_query().all()]}, HTTPStatus.OK


def create_aggregator(parameters: dict):
    new_query_id = new_aggregator(parameters['id'])

    return list(map(str, aggregators_query(new_query_id).all())), HTTPStatus.CREATED


def remove_aggregator(parameters: dict):
    delete_aggregator(parameters['id'])

    return _create_successful_response(
        status_code=HTTPStatus.OK,
        message='successfully removed',
    )
