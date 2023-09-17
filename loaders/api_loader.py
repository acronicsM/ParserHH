import time
import json
from environment import DUMPS_FOLDER, PAGE_FILENAME, HEADER, DETAIL_FILENAME
from common import Vacancy, exists_and_makedir, get_json_data, save_vacancy_from_json, update_detail_vacancy, \
    delete_expired_vacancies, get_vacancy_for_update_bin, save_vacancy_from_db
from parsers.api_parser import parse_detail_data
from parsers.currency_exchange_rate_parser import current_course


def load_page(app, query: str, do_dump: bool, per_page: int = 100, page: int = 0, courses=None) -> tuple[int, int]:
    params = {
        'text': query,
        'per_page': per_page,
        'search_field': 'name',
        'page': page,
    }

    data_json = get_json_data(header=HEADER, params=params)

    if do_dump:
        exists_and_makedir(DUMPS_FOLDER)
        with open(fr'{DUMPS_FOLDER}\{PAGE_FILENAME}{page}.json', 'w') as fp:
            json.dump(data_json, fp)

    if app:
        save_vacancy_from_db(app, data_json, courses)
    else:
        save_vacancy_from_json(data_json, courses)

    return data_json['found'], len(data_json['items'])


def pages_loader(app, query_vac: str, per_page: int = 100, logging: bool = False, do_dump: bool = False):

    courses = current_course()
    vacancies_processed = 0
    total_vacancies = 1
    page = 0

    while vacancies_processed < total_vacancies:
        if logging:
            print(f'Парсинг страницы {page}')

        _total_vacancies, _vacancies_processed = load_page(app=app,
                                                           query=query_vac,
                                                           per_page=per_page,
                                                           page=page,
                                                           do_dump=do_dump,
                                                           courses=courses
                                                           )
        total_vacancies = _total_vacancies
        vacancies_processed += _vacancies_processed
        page += 1

    if logging:
        print(f'Получено {vacancies_processed} вакансия из {total_vacancies}')

    return vacancies_processed, total_vacancies


def load_detail(vac_id: int, do_dump: bool):

    data_json = get_json_data(uri=str(vac_id))

    if do_dump:
        with open(fr'{DUMPS_FOLDER}\{DETAIL_FILENAME}{vac_id}.json', 'w') as fp:
            json.dump(data_json, fp)

    return data_json


def update_detail(vacancies: list[Vacancy], do_dump: bool = False, logging: bool = False):
    counter = 0
    timeout = 5
    delta = 2
    package = 5
    for vacancy in vacancies:
        counter += 1

        if logging:
            print(f'Детальный парсинг вакансии {vacancy.vac_id} ({counter} из {len(vacancies)})')

        data_json = load_detail(vacancy.vac_id, do_dump)

        if data_json is None:
            if logging:
                print(f'Не удалось получить детальные данные вакансии {vacancy.vac_id}')
            continue

        update_detail_vacancy(vacancy, parse_detail_data(data_json))

        vacancy.save()

        if counter % package == 0:
            time.sleep(timeout)
            timeout += delta
            if logging:
                print(f'Таймаут {timeout}')


def update_vacancy(query, do_dump: bool = False, logging: bool = False, app=None):
    pages_loader(query_vac=query, logging=logging, do_dump=do_dump, app=app)

    delete_expired_vacancies(logging=logging)

    update_detail(vacancies=get_vacancy_for_update_bin(), logging=logging, do_dump=do_dump)

