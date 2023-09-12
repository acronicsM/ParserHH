from common import Vacancy
from environment import REQUIRED_SKILLS

from bs4 import BeautifulSoup
import re


def parser_description_to_key_skills(description: str):
    pattern = r'[a-zA-Z]{1,}[ -]?[a-zA-Z]{1,}'

    description_skills = basic_skills = set()

    soup = BeautifulSoup(description, 'html.parser')
    for ul in soup.findAll('ul'):
        name = ul.find_previous('p')
        if name is None:
            name = ul.find_previous('strong')

        for child in ul.findChildren('li', recursive=False):
            for match in re.finditer(pattern, child.text, re.MULTILINE):
                skill = match.group()
                description_skills.add(skill)
                if name in REQUIRED_SKILLS:
                    basic_skills.add(skill)

    return description_skills, basic_skills


def parse_detail_data(data_json: dict):
    description_skills, basic_skills = parser_description_to_key_skills(data_json['description'])

    result = {
        'schedule': data_json['schedule']['name'],
        'description': data_json['description'],
        'key_skills': {i['name'] for i in data_json['key_skills']}  if data_json['key_skills'] else set(),
        'description_skills': description_skills,
        'basic_skills': basic_skills,
        'need_update': False
    }

    return result
