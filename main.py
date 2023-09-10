import requests
import json
import bs4
import os
import re
from datetime import datetime

Header = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 '
              'Safari/537.36 OPR/86.0.4363.59 (Edition Yx 05)'}

URI_vacancies = 'https://api.hh.ru/vacancies'
HH_vacancies_list_Folder = 'Page_HH_vacancies'


def hh_vacancies_list_requests_and_dump(query: str, per_page: int = 100, page: int = 0) -> tuple[int, int]:
    params = {
        'text': query,
        'per_page': per_page,
        'search_field': 'name',
        'page': page,
    }

    # Первый реквест для понимая общего количества вакансий
    raw_json = requests.get(URI_vacancies, params=params, headers=Header).json()
    with open(fr'{HH_vacancies_list_Folder}\hh{page}.json', 'w') as fp:
        json.dump(raw_json['items'], fp)

    return raw_json['found'], len(raw_json['items'])


def vacancies_list(query: str, per_page: int = 100) -> tuple[int, int]:
    vacancies_processed, total_vacancies, page = 0, 1, 0
    while vacancies_processed < total_vacancies:
        _total_vacancies, _vacancies_processed = hh_vacancies_list_requests_and_dump(query, per_page, page)
        total_vacancies = _total_vacancies
        vacancies_processed += _vacancies_processed

    return vacancies_processed, total_vacancies


def hh_vacancies_list_load():
    pattern = r'hh[0-9]*.json'
    vacs_dict = dict()
    for f in os.listdir(HH_vacancies_list_Folder):
        full_path = HH_vacancies_list_Folder + '/' + f
        if not os.path.isfile(full_path) or re.fullmatch(pattern, f) is None:
            continue

        with (open(full_path, 'r') as fp):
            for i in json.load(fp):
                vacs_dict[i['id']] = {
                    'name': i['name'],
                    'salary_from': i['salary']['from'] if i['salary'] else None,
                    'salary_to': i['salary']['to'] if i['salary'] else None,
                    'type': i['type']['name'],
                    'published_at': i['published_at'],  # datetime.fromisoformat(i['published_at'])
                    'archived': i['archived'],
                    'requirement': i['snippet']['requirement'],
                    'responsibility': i['snippet']['responsibility'],
                    'experience': i['experience']['name'],
                    'employment': i['employment']['name'],
                }

    with open(fr'{HH_vacancies_list_Folder}\HH_json_vacs.json', 'w') as fp:
        json.dump(vacs_dict, fp)


if __name__ == '__main__':

    # vac_processed, total_vac = vacancies_list('Python junior')
    # print(f'Получено {vac_processed} вакансия из {total_vac}')
    hh_vacancies_list_load()

