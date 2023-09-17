import json
from HH_parser.common import get_dump_files, save_vacancy_from_json, Vacancy, update_detail_vacancy
from HH_parser.environment import PAGE_FILENAME, DETAIL_FILENAME
from HH_parser.parsers.api_parser import parse_detail_data


def pages_loader():
    vacancies_processed = total_vacancies = 0
    for path in get_dump_files(f'{PAGE_FILENAME}[0-9]*.json'):
        with open(path, 'r') as fp:
            data_json = json.load(fp)
            save_vacancy_from_json(data_json)

            total_vacancies = data_json['found']
            vacancies_processed += len(data_json['items'])

    return vacancies_processed, total_vacancies


def update_detail(vacancies: list[Vacancy], logging: bool = False):
    counter = 0
    for vacancy in vacancies:
        counter += 1

        if logging:
            print(f'Детальный парсинг вакансии {vacancy.vac_id} ({counter} из {len(vacancies)})')

        for path in get_dump_files(f'{DETAIL_FILENAME}[0-9]*.json'):
            with open(path, 'r') as fp:
                data_json = json.load(fp)

        if data_json is None:
            if logging:
                print(f'Не удалось получить детальные данные вакансии {vacancy.vac_id}')
            continue

        update_detail_vacancy(vacancy, parse_detail_data(data_json))

        vacancy.save()
