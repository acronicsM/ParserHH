from datetime import datetime, timedelta

from ...models import Vacancy, Query, SkillsVacancy, Skills
from ... import db


def all_vacancies_query(page=0, per_page=10, tag_id=None, query_id=None, new_vacancies=False):
    if query_id:
        query = db.session.query(Vacancy).join(Vacancy.querys).filter(Query.id == query_id)
    else:
        query = Vacancy.query

    if tag_id:
        query = query.join(SkillsVacancy).join(Skills, SkillsVacancy.skill_id == Skills.id).filter(Skills.id == tag_id)

    if new_vacancies:
        _before = datetime.now() - timedelta(days=1)
        query = query.filter(Vacancy.published_at > _before)

    return query.count(), query.offset(page * per_page).limit(per_page)


def get_vacancy_query(vacancy_id):
    return Vacancy.query.get(vacancy_id)
