import requests
import json


def requests_and_dump(query: str,
                      uri: str,
                      per_page: int = 100,
                      page: int = 0,
                      header: dict = None,
                      folder: str = '.'
                      ) -> tuple[int, int]:
    if not header:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx 05)'}

    params = {
        'text': query,
        'per_page': per_page,
        'search_field': 'name',
        'page': page,
    }

    raw_json = requests.get(uri, params=params, headers=header).json()

    with open(fr'{folder}\hh{page}.json', 'w') as fp:
        json.dump(raw_json['items'], fp)

    return raw_json['found'], len(raw_json['items'])


def load_vacancies(query: str,
                   per_page: int = 100,
                   header: dict = None,
                   folder: str = '.'
                   ) -> tuple[int, int]:

    uri = 'https://api.hh.ru/vacancies'
    vacancies_processed, total_vacancies, page = 0, 1, 0
    while vacancies_processed < total_vacancies:
        _total_vacancies, _vacancies_processed = requests_and_dump(query=query,
                                                                   uri=uri,
                                                                   per_page=per_page,
                                                                   page=page,
                                                                   header=header,
                                                                   folder=folder
                                                                   )
        total_vacancies = _total_vacancies
        vacancies_processed += _vacancies_processed

    return vacancies_processed, total_vacancies
