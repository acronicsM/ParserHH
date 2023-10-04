from my_api import api
from flask_restx import fields, Namespace

aggregatorsCtrlr = Namespace(
    'Aggregators', path="/Aggregators", description='Агрегаторы вакансий')

createAggregatorsCommand = aggregatorsCtrlr.model('Create Todo command', {
    'id': fields.String(required=True, description='Todo details')
})

updateAggregatorsCommand = aggregatorsCtrlr.model('Update Todo command', {
    'id': fields.String(required=True, description='Todo details')
})

aggregatorsDto = aggregatorsCtrlr.model('Todo DTO', {
    'id': fields.Integer(description='Id of Todo'),
})


api.add_namespace(aggregatorsCtrlr)