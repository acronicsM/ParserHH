from my_api.models import Vacancy, Skills, SkillsVacancy, Query, vacancy_query
from my_api import db
from sqlalchemy import func, case, desc, select


def maximum_salary_for_querys():
    return db.session.query(
        db.func.max(Vacancy.salary_from).label('vacancy_salary_from'),
        db.func.max(Vacancy.salary_to).label('vacancy_salary_to'),
        db.func.count(Vacancy.id).label('vacancy_count'),
        Query.id.label('query_id'),
        Query.name.label('query_name')
    ).outerjoin(
        vacancy_query, Query.id == vacancy_query.c.query_id
    ).outerjoin(
        Vacancy, Vacancy.id == vacancy_query.c.vacancy_id
    ).group_by(Query.id)


def min_salary_for_querys(column):
    return db.session.query(
        db.func.min(column).label('min_value'),
        Query.id.label('query_id'),
        Query.name.label('query_name')
    ).outerjoin(
        vacancy_query,
        Query.id == vacancy_query.c.query_id,
    ).outerjoin(
        Vacancy,
        db.and_(
            Vacancy.id == vacancy_query.c.vacancy_id,
            column > 0
        ),
    ).group_by(Query.id)


def all_skills():
    skills_query = Skills.query.join(Skills.skill_vacancies).group_by(Skills.id)
    skills_query = skills_query.order_by(db.func.count(SkillsVacancy.skill_id).desc())

    return skills_query


def all_vacancies(tag_id=None, query_id=None):
    if query_id:
        query = db.session.query(Vacancy).join(Vacancy.querys).filter(Query.id == query_id)
    else:
        query = Vacancy.query

    if tag_id:
        query = query.join(SkillsVacancy).join(Skills, SkillsVacancy.skill_id == Skills.id).filter(Skills.id == tag_id)

    return query


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
