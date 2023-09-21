from pathlib import Path
from os import environ, path
from dotenv import load_dotenv

basedir = Path(__file__).parents[0]
load_dotenv(basedir / '.env')


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = basedir / 'static'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///base1.db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:adminadmin@localhost:5432/hh'

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


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///base1.db'
