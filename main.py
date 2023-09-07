import requests
import json

Header = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 '
              'Safari/537.36 OPR/86.0.4363.59 (Edition Yx 05)'}


def search_vacancies_id(query: str):
    params = {
        'text': query,
        'per_page': 100,
        'search_field': 'name',
        'page': 0,
    }
    uri_list = 'https://api.hh.ru/vacancies'

    for i in range(40):
        params['page'] = i
        raw_json = requests.get(uri_list, params=params, headers=Header).json()
        with open(f'hh{i}.json', 'w') as fp:
            json.dump(raw_json, fp)

search_vacancies_id('Python junior')
