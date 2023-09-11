import json
from environment import DUMPS_FOLDER, DO_DUMP, Page_FILENAME
from common import Vacancy, exists_and_makedir, get_json_data, save_vacancy


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

    raw_json = get_json_data(header=header, params=params)

    if do_dump:
        exists_and_makedir(folder)
        with open(fr'{folder}\{Page_FILENAME}{page}.json', 'w') as fp:
            json.dump(raw_json['items'], fp)

    for v in raw_json['items']:
        save_vacancy(vacancy=Vacancy(vac_id=v['id'], name=v['name'], raw_json=v))

    return raw_json['found'], len(raw_json['items'])


def load_vacancies(query_vac: str,
                   per_page: int = 100,
                   header: dict = None,
                   folder: str = None,
                   do_dump: bool = None,
                   ) -> tuple[int, int]:
    vacancies_processed, total_vacancies, page = 0, 1, 0
    while vacancies_processed < total_vacancies:
        _total_vacancies, _vacancies_processed = requests_and_parse_list(query_vac=query_vac,
                                                                         per_page=per_page,
                                                                         page=page,
                                                                         header=header,
                                                                         folder=folder,
                                                                         do_dump=do_dump
                                                                         )
        total_vacancies = _total_vacancies
        vacancies_processed += _vacancies_processed

    return vacancies_processed, total_vacancies


if __name__ == '__main__':

    query = 'Python junior'

    vac_processed, total_vac = load_vacancies(query_vac=query)
    print(f'Получено {vac_processed} вакансия из {total_vac}')
