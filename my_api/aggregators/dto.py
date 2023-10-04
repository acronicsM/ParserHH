from flask_restx import Model
from flask_restx.fields import String
from flask_restx.reqparse import RequestParser

from http import HTTPStatus


def validate_id(value):
    # Ваша проверка аргумента "id"
    if not value:
        raise HTTPStatus.BAD_REQUEST
    # Другие проверки...


create_aggregator_reqparser = RequestParser(bundle_errors=True)
create_aggregator_reqparser.add_argument("id",
                                         type=str,
                                         location="form",
                                         required=True,
                                         nullable=False,
                                         help="Invalid value for 'id'",)
                                         # error="This field is required",
                                         # callback=validate_id)

# update_tree_reqparser = create_tree_reqparser.copy()
# update_tree_reqparser.remove_argument('scientific_name')

aggregators_model = Model('Aggregators', {'id': String(required=True)})
