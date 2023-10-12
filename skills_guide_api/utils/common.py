from pathlib import Path
import requests
from flask import jsonify
from skills_guide_api import db, app
from . import querys


def create_successful_response(status_code, message):
    response = jsonify(status="success", message=message)
    response.status_code = status_code
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


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
