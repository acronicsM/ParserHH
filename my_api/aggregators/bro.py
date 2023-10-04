from http import HTTPStatus

from flask import jsonify
from flask_restx import abort, marshal

from my_api import db
from my_api.models import Aggregators
from my_api.aggregators.dto import aggregators_model


def _create_successful_response(status_code, message):
    response = jsonify(
        status="success",
        message=message,
    )
    response.status_code = status_code
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


def create_aggregator(parameters:dict):
    parameters['id'] = parameters['id'].upper()

    if Aggregators.query.get(parameters['id']):
        abort(HTTPStatus.CONFLICT, f"{parameters['id']} is already entered", status="fail")
    new_aggregator = Aggregators(**parameters)
    db.session.add(new_aggregator)
    db.session.commit()
    return _create_successful_response(
        status_code=HTTPStatus.CREATED,
        message='successfully created',
    )


def retrieve_aggregators_list():
    data = Aggregators.query.all()
    response_data = marshal(data, aggregators_model)
    response = jsonify(response_data)
    return response
