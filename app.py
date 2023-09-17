from datetime import datetime

import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

from common import get_all_vacancies
from loaders.api_loader import update_vacancy
from data_analysis import save_images

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgre:postgre@localhost/hh"

db = SQLAlchemy(app)


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __repr__(self):
        return f'query: {self.name} [{self.id}]'


class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    salary_from = db.Column(db.Float)
    salary_to = db.Column(db.Float)
    type = db.Column(db.String(100))
    published_at = db.Column(db.DateTime)
    requirement = db.Column(db.String)
    responsibility = db.Column(db.String)
    experience = db.Column(db.String)
    employment = db.Column(db.String)
    description = db.Column(db.String)
    schedule = db.Column(db.String)
    need_update = db.Column(db.Boolean)
    relevance_date = db.Column(db.DateTime, default=datetime.utcnow)
    currency = db.Column(db.String(3))

    def __repr__(self):
        return f'{self.id} {self.name}'

    # key_skills = db.Column(db.String)
    # description_skills = db.Column(db.String)
    # basic_skills = db.Column(db.String)


class skills(db.Model):
    vacancy = db.Column(db.Integer, db.ForeignKey(Vacancy.id))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    key_skills = db.Column(db.Boolean)
    description_skills = db.Column(db.Boolean)
    basic_skills = db.Column(db.Boolean)




@app.route('/')
def home():
    return 'welcome'


@app.route('/update_vacancy')
def get_update_vacancy():
    # /update_vacancy?query='query'&do_dump=True&logging=True

    do_dump = logging = False

    if _do_dump := request.args.get('do_dump'):
        do_dump = _do_dump

    if _logging := request.args.get('logging'):
        logging = _logging

    if query := request.args.get('query'):
        update_vacancy(query=query, do_dump=do_dump, logging=logging)
    else:
        return 'no key "query"', 400

    return 'done'


@app.route('/get_all_vacancy')
def get_all_vacancy():
    # /get_all_vacancy?per_page=100&page=0

    per_page, page = 100, 0

    if _per_page := request.args.get('per_page'):
        per_page = _per_page if _per_page <= per_page else per_page

    if _page := request.args.get('page'):
        page = _page

    result = jsonify(get_all_vacancies())

    return result

# 5432 adminadmin
@app.route('/get_vacancy/<int:vacancy_id>')
def get_vacancy(vacancy_id):
    # /get_vacancy/123456

    return 'In development'


@app.route('/get_images')
def get_images():
    return jsonify(save_images()), 200


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)