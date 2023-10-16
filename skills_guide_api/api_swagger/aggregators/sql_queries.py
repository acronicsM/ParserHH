from http import HTTPStatus
from flask_restx import abort

from skills_guide_api.models import Aggregators
from skills_guide_api import db
from ...utils.sql_queries import flush


def aggregators_query(agg_id=None):
    query = Aggregators.query

    if agg_id:
        query = query.filter_by(id=agg_id)

    return query


def new_aggregator(agg_id: str):
    aggregators_query(agg_id).first()
    if aggregators_query(agg_id).first():
        abort(HTTPStatus.CONFLICT, message=f"{agg_id} is already entered", status="fail")

    new = Aggregators(id=agg_id)
    db.session.add(new)

    if not flush():
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, status="fail")

    db.session.commit()

    return new.id


def delete_aggregator(agg_id: int):
    obj = aggregators_query(agg_id).first()
    if not obj:
        abort(HTTPStatus.CONFLICT, message=f"{agg_id} not found", status="fail")

    db.session.delete(obj)

    if not flush():
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, status="fail")

    db.session.commit()
