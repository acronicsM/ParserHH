from datetime import datetime
from . import db

vacancy_query = db.Table('vacancy_query',
                         db.Column('vacancy_id', db.Integer, db.ForeignKey('vacancy.id')),
                         db.Column('query_id', db.Integer, db.ForeignKey('query.id'))
                         )


class Aggregators(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    vacancies = db.relationship('Vacancy', backref='aggregator', lazy=True)

    def __str__(self):
        return self.id


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

    aggregator_id = db.Column(db.Integer, db.ForeignKey(Aggregators.id))

    querys = db.relationship('Query',
                             secondary=vacancy_query,
                             backref=db.backref('vacancies', lazy='dynamic')
                             )

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
