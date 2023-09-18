from datetime import datetime, timedelta
from pathlib import Path
import requests
from .environment import BASE_URI, HEADER
from .models import Vacancy
from . import db


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):

    if not header:
        header = HEADER

    return requests.get(url=(BASE_URI + f'/{uri}/') if uri else BASE_URI, params=params, headers=header).json()


def get_all_vacancies(page=None, per_page=10):
    if page:
        return Vacancy.query.offset(page*per_page).limit(per_page).all()
    else:
        return Vacancy.query.all()


def delete_expired_vacancies():
    now_minus_1_day = datetime.now() - timedelta(days=1)

    for vacancy in get_all_vacancies():
        if vacancy.relevance_date < now_minus_1_day:
            db.session.delete(vacancy)
