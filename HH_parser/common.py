from datetime import datetime, timedelta
import pickle
from pathlib import Path
import requests
from .environment import VACANCY_FOLDER, BASE_URI, HEADER, DUMPS_FOLDER
from .models import Vacancy, Skills
from . import db


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):

    if not header:
        header = HEADER

    return requests.get(url=(BASE_URI + f'/{uri}/') if uri else BASE_URI, params=params, headers=header).json()


def get_vacancies_file():
    return Path(VACANCY_FOLDER).glob('[0-9]*.bin')


def get_vacancy_obj(path: str) -> Vacancy | None:
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def get_dump_files(pattern: str):
    return Path(DUMPS_FOLDER).glob(pattern)


def get_vacancy_for_update():
    return Vacancy.query.filter(Vacancy.need_update).all()


def save_vacancy_from_db(data_json: dict, courses: dict | None = None) -> None:
    for v in data_json['items']:
        vacancy = Vacancy.query.get(vac_id := v['id'])
        if vacancy:
            vacancy.relevance_date = datetime.now()
        else:
            vacancy = Vacancy(id=vac_id, name=v['name'])
            vacancy.parser_raw_json(raw_json=v, courses=courses)

        db.session.add(vacancy)
        # db.session.flush()
        db.session.commit()


def update_detail_vacancy(vacancy: Vacancy, detail_data: dict):
    vacancy.schedule = detail_data['schedule']
    vacancy.description = detail_data['description']
    vacancy.need_update = False

    # all_ski
    #
    # for skill in detail_data['key_skills']:
    #     if skill
    #     _skill = Skills()
    # Skills.query.get
    # vacancy.key_skills = detail_data['key_skills']
    # vacancy.description_skills = detail_data['description_skills']
    # vacancy.basic_skills = detail_data['basic_skills']


def get_all_vacancies():
    return Vacancy.query.all()


def delete_expired_vacancies():
    now_minus_1 = datetime.now() - timedelta(days=1)

    for vacancy in get_all_vacancies():
        if vacancy.relevance_date < now_minus_1:
            db.session.delete(vacancy)
