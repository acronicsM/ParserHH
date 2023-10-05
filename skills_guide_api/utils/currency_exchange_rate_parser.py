import requests
from my_api import app


def current_course():
    url = 'http://cbrates.rbc.ru/tsv/cb/'
    courses = dict()
    for currency, code in app.config['CURRENCY_CLASSIFIER'].items():
        response = requests.get(url=f'{url}{code}.tsv', headers=app.config['HEADER'])

        if response.status_code != 200:
            courses[currency] = 1
        else:
            data_course = response.text
            data_course = data_course[data_course.rfind('\n'):].split('\t')
            courses[currency] = float(data_course[2]) / float(data_course[1])

    return courses


if __name__ == '__main__':
    print(current_course())
