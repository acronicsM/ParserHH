from http import HTTPStatus
from flask_restx import abort

from skills_guide_api.models import Vacancy, Query, vacancy_query
from skills_guide_api import db
from skills_guide_api.utils.querys import flush


def max_salary_query(id_filter=None):
    query = db.session.query(
        db.func.max(Vacancy.salary_from).label('vacancy_salary_from'),
        db.func.max(Vacancy.salary_to).label('vacancy_salary_to'),
        db.func.count(Vacancy.id).label('vacancy_count'),
        Query.id.label('query_id'),
        Query.name.label('query_name')
    ).outerjoin(
        vacancy_query, Query.id == vacancy_query.c.query_id
    ).outerjoin(
        Vacancy, Vacancy.id == vacancy_query.c.vacancy_id
    )

    if id_filter:
        query = query.filter(Query.id == id_filter)

    return query.group_by(Query.id)


def _min_salary_query(column, id_filter):
    query = db.session.query(
        db.func.min(column).label('min_value'),
        Query.id.label('query_id'),
        Query.name.label('query_name')
    ).outerjoin(
        vacancy_query,
        Query.id == vacancy_query.c.query_id,
    ).outerjoin(
        Vacancy,
        db.and_(
            Vacancy.id == vacancy_query.c.vacancy_id,
            column > 0
        ),
    )

    if id_filter:
        query = query.filter(Query.id == id_filter)

    return query.group_by(Query.id)


def min_salary_query(id_filter=None):
    return _min_salary_query(Vacancy.salary_from, id_filter), _min_salary_query(Vacancy.salary_to, id_filter)


def new_query(name: str):
    if Query.query.filter_by(name=name).first():
        abort(HTTPStatus.CONFLICT, message=f"{name} is already entered", status="fail")

    new = Query(name=name)
    db.session.add(new)

    if not flush():
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, status="fail")

    db.session.commit()

    return new.id


def delete_query(query_id: int):
    obj = Query.query.get(query_id)
    if not obj:
        abort(HTTPStatus.CONFLICT, message=f"{query_id} not found", status="fail")

    db.session.delete(obj)

    if not flush():
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, status="fail")

    db.session.commit()


def vacancies_query(query_id: int):
    return db.session.get(Query, query_id).vacancies
