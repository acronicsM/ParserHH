from pathlib import Path
from os import environ
from dotenv import load_dotenv

basedir = Path(__file__).parents[0]
load_dotenv(basedir / '.env')


class Config(object):

    # FLASK_APP = environ.get('FLASK_APP', default='app.py')
    ENV = environ.get('ENV', default='production')
    DEBUG = environ.get('DEBUG', default=False) == 'True'
    SECRET_KEY = environ.get('SECRET_KEY', default='dsfdsf4dffdsf4DFdf09034DSFf343edcfVbhkmnnppp')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', default='sqlite:///base1.db')

    SQLALCHEMY_RECORD_QUERIES = ENV == 'development'

    STATIC_FOLDER = basedir / 'static'

    HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx 05)'}

    BASE_URI = 'https://api.hh.ru/vacancies'

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

    GLOSSARY = ('key_skills', 'description_skills', 'basic_skills')

    TIMEOUT_DETAIL_LOADER = 5
    DELTA_DETAIL_LOADER = 2
    PACKAGE_DETAIL_LOADER = 5

    COUNT_TOP_VACANCIES = 4
    COUNT_TOP_SKILLS = 12

    AGGREGATORS = ['HH', 'HABR']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///base1.db'
