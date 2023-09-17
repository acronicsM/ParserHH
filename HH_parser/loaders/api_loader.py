import time
import json
from HH_parser.environment import DUMPS_FOLDER, HEADER, DETAIL_FILENAME
from HH_parser.common import Vacancy, get_json_data, update_detail_vacancy, save_vacancy_from_db, delete_expired_vacancies, get_vacancy_for_update
from HH_parser.parsers.api_parser import parse_detail_data
from HH_parser.parsers.currency_exchange_rate_parser import current_course


def load_page(query: str, per_page: int = 100, page: int = 0, courses=None) -> tuple[int, int]:
    params = {
        'text': query,
        'per_page': per_page,
        'search_field': 'name',
        'page': page,
    }

    data_json = get_json_data(header=HEADER, params=params)

    save_vacancy_from_db(data_json, courses)

    return data_json['found'], len(data_json['items'])


def pages_loader(query_vac: str, per_page: int = 100):

    courses = current_course()

    vacancies_processed = 0
    total_vacancies = 1
    page = 0

    while vacancies_processed < total_vacancies:
        _total_vacancies, _vacancies_processed = load_page(query=query_vac,
                                                           per_page=per_page,
                                                           page=page,
                                                           courses=courses
                                                           )
        total_vacancies = _total_vacancies
        vacancies_processed += _vacancies_processed
        page += 1

    return vacancies_processed, total_vacancies


def update_detail(vacancies: list[Vacancy]):
    counter = 0
    timeout = 5
    delta = 2
    package = 5
    for vacancy in vacancies:
        counter += 1

        data_json = get_json_data(uri=str(vacancy.id))

        if data_json is None:
            continue

        update_detail_vacancy(vacancy, parse_detail_data(data_json))

        # vacancy.save()

        if counter % package == 0:
            time.sleep(timeout)
            timeout += delta


def update_vacancy(query,):
    pages_loader(query_vac=query)

    delete_expired_vacancies()

    update_detail(vacancies=get_vacancy_for_update())

