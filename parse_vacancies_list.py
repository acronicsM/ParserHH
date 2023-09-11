import json
from environment import DUMPS_FOLDER, DO_DUMP, Page_FILENAME
from common import Vacancy, exists_and_makedir, get_json_data, save_vacancy, get_dump_files


def requests_and_parse_list(query_vac: str,
                            per_page: int = 100,
                            page: int = 0,
                            header: dict = None,
                            folder: str = None,
                            do_dump: bool = None
                            ) -> tuple[int, int]:

    if not folder:
        folder = DUMPS_FOLDER

    if do_dump is None:
        do_dump = DO_DUMP

    params = {
        'text': query_vac,
        'per_page': per_page,
        'search_field': 'name',
        'page': page,
    }

    data_json = get_json_data(header=header, params=params)

    if do_dump:
        exists_and_makedir(folder)
        with open(fr'{folder}\{Page_FILENAME}{page}.json', 'w') as fp:
            json.dump(data_json, fp)

    save_vacancy_from_json(data_json)

    return data_json['found'], len(data_json['items'])


def load_vacancies(query_vac: str,
                   per_page: int = 100,
                   header: dict = None,
                   folder: str = None,
                   do_dump: bool = None,
                   from_dump: bool = None,
                   logging: bool = False
                   ) -> tuple[int, int]:

    if from_dump:
        return get_page_data_from_dump()

    vacancies_processed, total_vacancies, page = 0, 1, 0
    while vacancies_processed < total_vacancies:
        if logging:
            print(f'Парсинг страницы {page}')

        _total_vacancies, _vacancies_processed = requests_and_parse_list(query_vac=query_vac,
                                                                         per_page=per_page,
                                                                         page=page,
                                                                         header=header,
                                                                         folder=folder,
                                                                         do_dump=do_dump,
                                                                         )
        total_vacancies = _total_vacancies
        vacancies_processed += _vacancies_processed
        page += 1

    return vacancies_processed, total_vacancies


def get_page_data_from_dump():
    vacancies_processed = total_vacancies = 0
    for path in get_dump_files('hh_page_[0-9]*.json'):
        with open(path, 'r') as fp:
            data_json = json.load(fp)
            save_vacancy_from_json(data_json)

            total_vacancies = data_json['found']
            vacancies_processed += len(data_json['items'])

    return vacancies_processed, total_vacancies


def save_vacancy_from_json(data_json: dict):
    for v in data_json['items']:
        save_vacancy(vacancy=Vacancy(vac_id=v['id'], name=v['name'], raw_json=v))


if __name__ == '__main__':

    query = 'Python junior'

    vac_processed, total_vac = load_vacancies(query_vac=query, from_dump=True)
    print(f'Получено {vac_processed} вакансия из {total_vac}')
