from datetime import datetime
from my_api import db

vacancy_query = db.Table('vacancy_query',
                         db.Column('vacancy_id', db.Integer, db.ForeignKey('vacancy.id')),
                         db.Column('query_id', db.Integer, db.ForeignKey('query.id'))
                         )


class Aggregator(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    class_name = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(50))
    vacancies = db.relationship('Vacancy', backref=db.backref('aggregator', lazy=True))


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

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

    querys = db.relationship('Query',
                             secondary=vacancy_query,
                             backref=db.backref('vacancies', lazy='dynamic')
                             )

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'published_at': self.published_at,
            'requirement': self.requirement,

        }

    def to_dict_detail(self):
        data = self.to_dict()
        data['experience'] = self.experience
        data['employment'] = self.employment
        data['description'] = self.description
        data['schedule'] = self.schedule

        return data

    def __repr__(self):
        return f'{self.id} {self.name}'


class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)


class SkillsVacancy(db.Model):
    vacancy_id = db.Column(db.Integer, db.ForeignKey(Vacancy.id))
    skill_id = db.Column(db.Integer, db.ForeignKey(Skills.id))
    id = db.Column(db.Integer, primary_key=True)
    key_skill = db.Column(db.Boolean, nullable=True, default=False)
    description_skill = db.Column(db.Boolean, nullable=True, default=False)
    basic_skill = db.Column(db.Boolean, nullable=True, default=False)

    skill = db.relationship('Skills', backref=db.backref('skill_vacancies', lazy=True))
    vacancy = db.relationship('Vacancy', backref=db.backref('skill_vacancies', lazy=True))

    def to_dict(self):
        return {
            'id': self.skill.id,
            'name': self.skill.name,
            'key': self.key_skill,
            'description': self.description_skill,
            'basic': self.basic_skill,
        }


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value_int = db.Column(db.Integer)


class TopVacancies(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class TopSkills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
