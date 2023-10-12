from skills_guide_api.models import Vacancy, Statistics, TopVacancies, TopSkills


def statistics_item_query(statistics_id):
    return Statistics.query.get(statistics_id)


def top_vacancies_query():
    for i in TopVacancies.query.all():

        pass
        Vacancy.query.get(i.id).to_dict()

    return [Vacancy.query.get(i.id).to_dict() for i in TopVacancies.query.all()]


def top_skills_query():
    return TopSkills.query
