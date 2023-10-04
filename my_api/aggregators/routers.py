from flask_restx import Resource, Namespace
from http import HTTPStatus

from my_api.aggregators.dto import create_aggregator_reqparser, aggregators_model
from my_api.aggregators.bro import retrieve_aggregators_list, create_aggregator

aggregators_ns = Namespace(name="aggregators", validate=True)

aggregators_model = aggregators_ns.model(aggregators_model.name, aggregators_model)


@aggregators_ns.route("")
@aggregators_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
@aggregators_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
class Aggregators(Resource):
    @aggregators_ns.response(int(HTTPStatus.OK), 'Retrieved aggregators list.')
    def get(self):
        """ Возвращает список агрегаторов """
        return retrieve_aggregators_list()

    @aggregators_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.' )
    @aggregators_ns.response(int(HTTPStatus.CREATED), 'Added new aggregator.')
    @aggregators_ns.response(int(HTTPStatus.CONFLICT), 'aggregator id already exists.')
    @aggregators_ns.expect(aggregators_model)
    def post(self):
        return create_aggregator(aggregators_ns.payload)

    @aggregators_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @aggregators_ns.response(int(HTTPStatus.OK), 'Aggregator removed.')
    @aggregators_ns.response(int(HTTPStatus.CONFLICT), 'Aggregator id already not exists.')
    @aggregators_ns.expect(create_aggregator_reqparser, validate=True)
    def delete(self):
        return create_aggregator(aggregators_ns.payload)
