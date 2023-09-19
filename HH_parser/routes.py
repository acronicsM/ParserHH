from . import app
from flask import request, jsonify

from .common import *
from .loaders.api_loader import update_vacancy
from .models import Query


@app.route('/')
def home():
    return 'welcome'


@app.route('/update_vacancy')
def get_update_vacancy():
    if query := request.args.get('query'):
        return jsonify(update_vacancy(query=query))
    else:
        if all_query := Query.query.all():
            return jsonify([update_vacancy(query=query) for query in all_query])
        else:
            return 'no key "query"', 400


@app.route('/vacancies')
def vacancies():
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
    return jsonify(get_vacancy_skills(vacancy_id))


@app.route('/get_tag_vacancies')
def get_tag_vacancies():
    if tag_name := request.args.get('tag_name'):
        return get_skill_vacancies(tag_name)

    return 'not arg "tag_name"', 400


@app.route('/tags',)
def tags():

    per_page, page = 10, 0

    if _per_page := request.args.get('per_page'):
        per_page = min(int(_per_page), per_page)

    if _page := request.args.get('page'):
        page = int(_page)

    return jsonify(get_all_skills(per_page=per_page, page=page))


@app.route('/query/<int:query_id>')
def query_vacancy(query_id):
    return jsonify(get_vacancy_query(query_id))


@app.route('/query', methods=['GET', 'POST', 'DELETE'])
def query():
    if request.method == 'GET':
        return jsonify(get_query())
    elif request.method == 'POST':
        if query_name := request.args.get('query_name'):
            post_query(query_name)
            return 'done'

        return 'not arg "query_name"', 400
    elif request.method == 'DELETE':
        if query_id := request.args.get('query_id'):
            delete_query(query_id)
            return 'done'

        return 'not arg "query_id"', 400

    return 'Method Not Allowed', 405


@app.route('/get_images')
def get_images():
    return 'work get_images'
