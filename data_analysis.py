from common import get_vacancies_file, get_vacancy_obj, Vacancy


def get_all_vacancies():
    return [get_vacancy_obj(path) for path in get_vacancies_file()]


def collect_data_skills(skills_dict: dict, skill: str, vacancy: Vacancy):
    if skill not in skills_dict:
        skills_dict[skill] = {'count_vacancy': 0, 'salary': set()}

    if vacancy.salary_from is not None:
        skills_dict[skill]['salary'].add(vacancy.salary_from)

    if vacancy.salary_to is not None:
        skills_dict[skill]['salary'].add(vacancy.salary_to)

    if vacancy.salary_from is not None and vacancy.salary_to is not None:
        skills_dict[skill]['salary'].add((vacancy.salary_from + vacancy.salary_to) / 2)

    skills_dict[skill]['count_vacancy'] += 1


if __name__ == '__main__':

    vacancies = get_all_vacancies()

    key_skills = description_skills = basic_skills = dict()

    for vacancy in vacancies:
        for skill in vacancy.key_skills:
            collect_data_skills(key_skills, skill, vacancy)

        for skill in vacancy.description_skills:
            collect_data_skills(description_skills, skill, vacancy)

        # for skill in vacancy.basic_skills:
        #     collect_data_skills(basic_skills, skill, vacancy)

    print(f'Всего вакансий: {len(vacancies)}')

    for skill, v in key_skills.items():
        min_salary, max_salary = min(v['salary']), max(v['salary'])
        average_salary = (min_salary + max_salary) / 2
        print(f'{skill}: {min_salary:_} {average_salary:_} {max_salary:_}')
    # print('key_skills', key_skills, '', sep='\n')
    # print('description_skills', description_skills, '', sep='\n')
    # print('basic_skills', basic_skills, '', sep='\n')

