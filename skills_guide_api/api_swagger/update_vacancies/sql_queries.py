from datetime import datetime, timedelta
from sqlalchemy import func, case, desc

from skills_guide_api import db, app
from ...utils.sql_queries import flush
from skills_guide_api.models import (Query, Aggregators, Vacancy, Statistics,
                                     TopVacancies, TopSkills, Skills, SkillsVacancy)


def all_queries():
    return Query.query


def get_query(query_id: int):
    return Query.query.get(query_id)


def all_aggregators():
    return Aggregators.query


def delete_expired_vacancies() -> tuple[int, bool]:
    now_minus_1_day = datetime.now() - timedelta(days=1)
    delete_vacancies = 0

    for vacancy in Vacancy.query.all():
        if vacancy.relevance_date < now_minus_1_day:
            db.session.delete(vacancy)
            delete_vacancies += 1

    return delete_vacancies, not flush()


def update_statistics():
    Statistics.query.delete()
    TopVacancies.query.delete()
    TopSkills.query.delete()

    db.session.add(Statistics(id=1, value_int=Vacancy.query.count()))
    db.session.add(Statistics(id=2, value_int=Skills.query.count()))

    for i in top_vacancies(app.config['COUNT_TOP_VACANCIES']).all():
        db.session.add(TopVacancies(id=i[0]))

    for i in top_skills(app.config['COUNT_TOP_SKILLS']).all():
        db.session.add(TopSkills(id=i[4], name=i[3], salary_max=i[1], salary_min=i[0]))

    return not flush()


def top_vacancies(count_vacancies: int):
    case_ = case((Vacancy.salary_from > Vacancy.salary_to, Vacancy.salary_from), else_=Vacancy.salary_to)

    vacancies = db.session.query(
        Vacancy.id,
        case_.label('max_salary')
    ).order_by(
        desc('max_salary')
    ).limit(count_vacancies)

    return vacancies


def top_skills(count_skills: int):
    case_from = case((Vacancy.salary_from == 0, Vacancy.salary_to), else_=Vacancy.salary_from)
    case_to = case((Vacancy.salary_to == 0, Vacancy.salary_from), else_=Vacancy.salary_to)

    query = db.session.query(
        func.min(case_from).label('salary_from'),
        func.max(case_to).label('salary_to'),
        func.max(Vacancy.id).label('count_vacancies'),
        Skills.name,
        Skills.id,
    ).join(
        SkillsVacancy, SkillsVacancy.vacancy_id == Vacancy.id
    ).join(
        Skills, SkillsVacancy.skill_id == Skills.id
    ).filter(
        (Vacancy.salary_from != 0) | (Vacancy.salary_to != 0),
    ).group_by(
        Skills.id,
        Skills.name
    ).order_by(
        desc('count_vacancies',)
    ).limit(count_skills)

    return query