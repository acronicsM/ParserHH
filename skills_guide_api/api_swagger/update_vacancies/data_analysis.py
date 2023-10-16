import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import case, desc, func

from ... import app, db
from ...utils.common import exists_and_makedir
from ...models import Vacancy, Skills, SkillsVacancy

review = app.config['STATIC_FOLDER'] / 'review'
glossary = app.config['GLOSSARY']
exists_and_makedir(review)


def skills_salary():
    case_ = case((Vacancy.salary_from > Vacancy.salary_to, Vacancy.salary_from), else_=Vacancy.salary_to)

    top_skills = db.session.query(
        Skills.name,
        case_.label('max_salary')
    ).join(
        SkillsVacancy, SkillsVacancy.skill_id == Skills.id
    ).join(
        Vacancy, SkillsVacancy.vacancy_id == Vacancy.id
    ).filter(
        (Vacancy.salary_from != 0) | (Vacancy.salary_to != 0),
    ).order_by(
        desc('max_salary')
    ).all()

    df = pd.DataFrame(top_skills, columns=['Навык', 'Зарплата'])

    plt.figure(figsize=(20, 15), dpi=200)
    sns.scatterplot(x='Зарплата', y='Навык', data=df)

    plt.savefig(fr'{review}\salary.jpg')


def skills_vacancy():
    top_skills = db.session.query(
        Skills.name,
        func.count(SkillsVacancy.vacancy_id).label('vacancy_count')
    ).join(
        SkillsVacancy, SkillsVacancy.skill_id == Skills.id
    ).join(
        Vacancy, SkillsVacancy.vacancy_id == Vacancy.id
    ).filter(
        Vacancy.salary_from != 0,
        Vacancy.salary_to != 0
    ).group_by(
        Skills.name
    ).order_by(
        desc('vacancy_count')
    ).all()

    df = pd.DataFrame(top_skills, columns=['Skills', 'Number of Vacancies'])

    plt.figure(figsize=(20, 15), dpi=200)
    sns.barplot(y='Skills', x='Number of Vacancies', data=df)

    plt.savefig(fr'{review}\vacancies.jpg')


def save_images():
    skills_salary()
    skills_vacancy()


if __name__ == "__main__":
    save_images()
