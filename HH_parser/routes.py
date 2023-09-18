from . import app
from flask import request, jsonify

from .common import get_all_vacancies, get_vacancy_by_id
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


@app.route('/vacancies')
def vacancies():
    # /get_all_vacancy?per_page=100&page=0

    per_page, page = 10, 0

    if _per_page := request.args.get('per_page'):
        per_page = min(int(_per_page), per_page)

    if _page := request.args.get('page'):
        page = int(_page)

    count, result = get_all_vacancies(page=page, per_page=per_page)

    return jsonify({'found': count,
                    'result': [vacancy.to_dict() for vacancy in result]
                    })


@app.route('/get_vacancy/<int:vacancy_id>')
def get_vacancy(vacancy_id):
    return jsonify(get_vacancy_by_id(vacancy_id).to_dict_detail())


@app.route('/get_vacancy_tags/<int:vacancy_id>')
def get_vacancy_tags(vacancy_id):
    return 'work get_vacancy_tags'


@app.route('/get_tag_vacancies/<int:tag_id>')
def get_tag_vacancies(tag_id):
    return 'work get_tag_vacancies'


@app.route('/get_all_tags')
def get_all_tags():
    return 'work get_all_tags'


@app.route('/post_new_query', methods=['POST'])
def post_new_query():
    return 'work post_new_query'


@app.route('/get_images')
def get_images():
    return 'work get_images'
