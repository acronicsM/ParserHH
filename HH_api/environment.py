
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx 05)'}

Page_FILENAME = 'hh_page_'
DETAIL_FILENAME = 'hh_detail_'

DUMPS_FOLDER = r'..\dumps'
VACANCY_FOLDER = r'..\vacancy'

BASE_URI = 'https://api.hh.ru/vacancies'

PATTERN = 'hh[0-9]*.json'

DO_DUMP = True

REQUIRED_SKILLS = [
    'Мы хотели бы, чтобы вы',
    'Чем предстоит заниматься',
    'Обязанности',
    'Требования',
    'Наши ожидания',
    'Мы ожидаем',
    'Что нам важно',
    'Hard skills',
    'Чего мы ждем',
    'Что нужно знать',
    'Что нужно от тебя',
    'Ожидаем',
]