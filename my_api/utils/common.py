from datetime import datetime, timedelta
from pathlib import Path
import requests

from my_api.models import Vacancy, Skills, Query, Statistics, TopVacancies, TopSkills, Aggregators
from my_api import db, app

from . import querys
from .http_status import status_500, status_208, status_200


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):
    if not header:
        header = app.config['HEADER']

    url = (app.config['BASE_URI'] + f'/{uri}/') if uri else app.config['BASE_URI']

    response = requests.get(url=url, params=params, headers=header).json()
    return response


def get_all_vacancies(page=0, per_page=10, tag_id=None, query_id=None):
    query = querys.all_vacancies(tag_id=tag_id, query_id=query_id)

    return query.count(), query.offset(page * per_page).limit(per_page).all()


def get_vacancy_by_id(vacancy_id):
    return db.session.get(Vacancy, vacancy_id)


def get_vacancy_skills(vacancy_id):
    vacancy = db.session.get(Vacancy, vacancy_id)
    if not vacancy:
        return []
    return [skill.to_dict() for skill in vacancy.skill_vacancies]


def get_skill_vacancies(skill_id):
    return [i.vacancy.to_dict() for i in Skills.query.get(skill_id).skill_vacancies]


def get_all_skills(page=0, per_page=10):
    skills_query = querys.all_skills()

    count = skills_query.count()

    skills_page = []
    for skill in skills_query.offset(page * per_page).limit(per_page).all():
        skills_page.append({
            'id': skill.id,
            'name': skill.name,
            'vacancies': len(skill.skill_vacancies),
            'key': sum(i.key_skill for i in skill.skill_vacancies),
            'description': sum(i.description_skill for i in skill.skill_vacancies),
            'basic': sum(i.basic_skill for i in skill.skill_vacancies),
        })

    return {'found': count, 'result': skills_page}


def delete_expired_vacancies() -> tuple[int, bool]:
    now_minus_1_day = datetime.now() - timedelta(days=1)
    delete_vacancies = 0

    for vacancy in get_all_vacancies()[1]:
        if vacancy.relevance_date < now_minus_1_day:
            db.session.delete(vacancy)
            delete_vacancies += 1

    return delete_vacancies, not querys.flush()


def get_vacancy_query(query_id):
    return [i.to_dict() for i in db.session.get(Query, query_id).vacancies.all()]


def get_query():
    max_salary = querys.maximum_salary_for_querys().all()
    min_salary_from = querys.min_salary_for_querys(Vacancy.salary_from).all()
    min_salary_to = querys.min_salary_for_querys(Vacancy.salary_to).all()

    response = {i[3]: {'name': i[4], 'count': i[2], 'max': max(i[0] if i[0] else 0, i[1] if i[1] else 0)} for i in
                max_salary}

    for i in min_salary_from:
        response[i[1]]['min'] = i[0] if i[0] else 0

    for i in min_salary_to:
        response[i[1]]['min'] = min(response[i[1]]['min'], (i[0] if i[0] else 0))

    return response


def post_query(name: str):
    if not Query.query.filter_by(name=name).first():
        db.session.add(Query(name=name))

        if querys.flush():
            db.session.commit()
        else:
            return status_500()
    else:
        return status_208(name)

    return status_200()


def delete_query(query_id):
    if query := Query.query.get(query_id):
        db.session.delete(query)

        if querys.flush():
            db.session.commit()
        else:
            return status_500(True)
    else:
        return status_208(query_id, True)

    return status_200()


def get_aggregators():
    return [str(i) for i in Aggregators.query.all()]


def post_aggregator(name: str):
    if not Aggregators.query.get(name):
        db.session.add(Aggregators(id=name.upper()))

        if querys.flush():
            db.session.commit()
        else:
            return status_500()
    else:
        return status_208(name)

    return status_200()


def delete_aggregator(name: str):
    if agg := Aggregators.query.get(id=name):
        db.session.delete(agg)

        if querys.flush():
            db.session.commit()
        else:
            return status_500(True)
    else:
        return status_208(name, True)

    return status_200()


def update_statistics():
    Statistics.query.delete()
    TopVacancies.query.delete()
    TopSkills.query.delete()

    db.session.add(Statistics(id=1, value_int=Vacancy.query.count()))
    db.session.add(Statistics(id=2, value_int=Skills.query.count()))

    for i in querys.top_vacancies(app.config['COUNT_TOP_VACANCIES']).all():
        db.session.add(TopVacancies(id=i[0]))

    for i in querys.top_skills(app.config['COUNT_TOP_SKILLS']).all():
        db.session.add(TopSkills(id=i[4], name=i[3], salary_max=i[1], salary_min=i[0]))

    return not querys.flush()


def index_data():
    return {
        'count_vacancies': Statistics.query.get(1).value_int,
        'count_skills': Statistics.query.get(2).value_int,
        'top_vacancies': [Vacancy.query.get(i.id).to_dict() for i in TopVacancies.query.all()],
        'top_skills': [{'min': i.salary_min, 'max': i.salary_max, 'name': i.name, 'id': i.id} for i in
                       TopSkills.query.all()]
    }


def update_vacancies(query: str | Query) -> dict:
    aggs = app.config['AGGREGATORS']
    response = {'delete_vacancies': -1, 'result': dict(), 'update_statistics': False}

    for agg in Aggregators.query.all():
        response[agg.id] = {'error': True}
        if agg.id in app.config['AGGREGATORS']:
            result = aggs[agg.id]().update_vacancy(query=query)
            if result['error']:
                return response

            response['result'][agg.id] = result

    delete_vacancies, deletion_error = delete_expired_vacancies()

    if deletion_error:
        return response

    if update_statistics():
        return response

    db.session.commit()

    response['delete_vacancies'] = delete_vacancies
    response['update_statistics'] = True

    return response
