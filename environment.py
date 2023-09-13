import pathlib


HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx 05)'}


PAGE_FILENAME = 'hh_page_'
DETAIL_FILENAME = 'hh_detail_'

DUMPS_FOLDER = r'dumps'
VACANCY_FOLDER = r'vacancy_data'

BASE_URI = 'https://api.hh.ru/vacancies'

PATTERN = 'hh[0-9]*.json'

DO_DUMP = True

REQUIRED_SKILLS = [
    'Мы хотели бы, чтобы вы',
    'Чем предстоит заниматься',
    'Обязанности',
    'Требования',
    'ожидания',
    'ожидаем',
    'важно',
    'Hard skills',
    'ждем',
    'нужно',
    'Ожидаем',
    'Что для этого требуется',
    'Необходимые знания',
]

CURRENCY_CLASSIFIER = {
    'RUB': 643,
    'RUR': 643,
    'USD': 840,
    'EUR': 978,
    'KZT': 398,
    'BYN': 933,
}
