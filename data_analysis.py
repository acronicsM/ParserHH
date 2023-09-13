from common import get_all_vacancies, Vacancy
import seaborn as sns



def create_collect_data_skills(skills_dict: dict, skill: str, vacancy: Vacancy):
    if skill not in skills_dict:
        skills_dict[skill] = {'count_vacancy': 0, 'salary': set()}

    skills_dict[skill]['salary'].add(vacancy.salary_from)
    skills_dict[skill]['salary'].add(vacancy.salary_to)
    skills_dict[skill]['salary'].add((vacancy.salary_from + vacancy.salary_to) / 2)

    skills_dict[skill]['count_vacancy'] += 1


def print_collect_data_skills(skills_dict: dict):
    for skill, v in skills_dict.items():
        min_salary, max_salary = min(v['salary']), max(v['salary'])
        average_salary = (min_salary + max_salary) / 2
        print(f'{skill}: {min_salary:_} {average_salary:_} {max_salary:_}')


def collect_data_skills(vacs: list[Vacancy]):
    key = dict()
    description = dict()
    basic = dict()

    for vacancy in vacs:
        for skill in vacancy.key_skills:
            create_collect_data_skills(key, skill, vacancy)

        for skill in vacancy.description_skills:
            create_collect_data_skills(description, skill, vacancy)

        for skill in vacancy.basic_skills:
            create_collect_data_skills(basic, skill, vacancy)

    return key, description, basic


if __name__ == '__main__':

    vacancies = get_all_vacancies()

    key_skills, description_skills, basic_skills = collect_data_skills(vacancies)

    print(f'Всего вакансий: {len(vacancies)}')

    print_collect_data_skills(basic_skills)
