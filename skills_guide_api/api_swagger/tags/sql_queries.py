from skills_guide_api.models import SkillsVacancy, Skills
from skills_guide_api import db


def all_skills_query(page=0, per_page=10):
    skills_query = Skills.query.join(Skills.skill_vacancies).group_by(Skills.id)
    skills_query = skills_query.order_by(db.func.count(SkillsVacancy.skill_id).desc())

    return skills_query.count(), skills_query.offset(page * per_page).limit(per_page)


def get_skill_query(skill_id):
    return Skills.query.get(skill_id)
