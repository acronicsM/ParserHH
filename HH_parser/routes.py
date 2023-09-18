from . import app
from flask import request
from .loaders.api_loader import update_vacancy
from .models import Query


@app.route('/')
def home():
    return 'welcome'


@app.route('/update_vacancy')
def get_update_vacancy():
    # /update_vacancy?query='query'

    if query := request.args.get('query'):
        update_vacancy(query=query)
        return 'done'
    else:

        all_query = Query.query.all()
        for query in all_query:
            update_vacancy(query=query)

        if all_query:
            return 'done'
        else:
            return 'no key "query"', 400


@app.route('/get_all_vacancy')
def get_all_vacancy():
    # /get_all_vacancy?per_page=100&page=0

    per_page, page = 100, 0

    if _per_page := request.args.get('per_page'):
        per_page = _per_page if int(_per_page) <= per_page else per_page

    if _page := request.args.get('page'):
        page = _page

    # result = jsonify(get_all_vacancies())

    return 'work get_all_vacancy'


@app.route('/get_vacancy/<int:vacancy_id>')
def get_vacancy(vacancy_id):
    # /get_vacancy/123456

    return 'In development'


@app.route('/get_images')
def get_images():
    return 'work get_images'
