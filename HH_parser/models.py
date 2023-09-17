from datetime import datetime
from . import db


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

    skills = db.relationship('Skills', backref='_vacancy', lazy=True)

    def parser_raw_json(self, raw_json, courses):
        published_at = raw_json['published_at']
        published_at = published_at[:published_at.find('+')]

        self.relevance_date = datetime.utcnow()
        self.need_update = True

        self.type = raw_json['type']['name']
        self.published_at = datetime.fromisoformat(published_at)
        self.requirement = raw_json['snippet']['requirement']
        self.responsibility = raw_json['snippet']['responsibility']
        self.experience = raw_json['experience']['name']
        self.employment = raw_json['employment']['name']

        if raw_json['salary']:
            self.currency = raw_json['salary']['currency']
            self.salary_from = raw_json['salary']['from'] if raw_json['salary']['from'] else 0
            self.salary_to = raw_json['salary']['to'] if raw_json['salary']['to'] else 0
        else:
            self.currency = 'RUB'
            self.salary_from = 0
            self.salary_to = 0

        if courses:
            course = courses[self.currency]
            if not course:
                print(f'Не удалось конвертировать валюту {self.currency}')
            else:
                self.salary_from = self.salary_from * course
                self.salary_to = self.salary_to * course

    def __repr__(self):
        return f'{self.id} {self.name}'


class Skills(db.Model):
    vacancy = db.Column(db.Integer, db.ForeignKey(Vacancy.id))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    key_skills = db.Column(db.Boolean)
    description_skills = db.Column(db.Boolean)
    basic_skills = db.Column(db.Boolean)
