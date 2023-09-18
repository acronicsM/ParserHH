from datetime import datetime, timedelta
from pathlib import Path
import requests
from .environment import BASE_URI, HEADER
from .models import Vacancy, Skills
from . import db


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):

    if not header:
        header = HEADER

    return requests.get(url=(BASE_URI + f'/{uri}/') if uri else BASE_URI, params=params, headers=header).json()


def get_all_vacancies(page=None, per_page=10):
    query = Vacancy.query

    count = query.count()

    if page is not None:
        query = query.offset(page * per_page).limit(per_page)

    return count, query.all()


def get_vacancy_by_id(vacancy_id):
    return db.session.get(Vacancy, vacancy_id)


def get_all_skills(page=None, per_page=10):
    query = Skills.query

    count = query.count()

    if page is not None:
        query = query.offset(page * per_page).limit(per_page)

    return count, query.all()


def delete_expired_vacancies():
    now_minus_1_day = datetime.now() - timedelta(days=1)

    for vacancy in get_all_vacancies():
        if vacancy.relevance_date < now_minus_1_day:
            db.session.delete(vacancy)



