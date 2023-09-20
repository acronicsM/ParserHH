from os import environ, path
from dotenv import load_dotenv

# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """Set Flask config variables."""

    # General Config
    # ENVIRONMENT = environ.get("ENVIRONMENT")
    # FLASK_APP = environ.get("FLASK_APP")
    # FLASK_DEBUG = environ.get("FLASK_DEBUG")
    # SECRET_KEY = environ.get("SECRET_KEY")
    # DEBUG = environ.get("DEBUG")
    STATIC_FOLDER = 'static'
    #
    # # Database
    # SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    #
    # # AWS Secrets
    # AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
    # AWS_KEY_ID = environ.get('AWS_KEY_ID')


HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx 05)'}

IMAGE_FOLDER = 'images'

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
