from common import get_all_vacancies, Vacancy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def add_skills_to_dict(vacancy: Vacancy, skills_dict: list, attr_name: str, attr_index: int):
    skill_str, salary_str = 'skills', 'salarys'
    for i in vacancy.__getattribute__(attr_name):
        if i not in skills_dict:
            skills_dict[i] = {skill_str: [0, 0, 0], salary_str: []}
            skills_dict[i][skill_str] = [0, 0, 0]

        skills_dict[i][skill_str][attr_index] += 1
        skills_dict[i][salary_str].append(vacancy.salary_to)
        skills_dict[i][salary_str].append(vacancy.salary_from)


def create_dataframe_from_vacancy():
    glossary = ('key_skills', 'description_skills', 'basic_skills')
    skills = dict()
    for vacancy in get_all_vacancies():
        for k, v in enumerate(glossary):
            add_skills_to_dict(vacancy, skills, v, k)

    skills_list = [(skill, *value['skills']) for skill, value in skills.items()]
    salarys_list = [(skill, v) for skill, value in skills.items() for v in value['salarys']]

    df_skills = pd.DataFrame(skills_list, columns=['skill', *glossary])
    df_salarys = pd.DataFrame(salarys_list, columns=['skill', 'salary'])

    print(df_skills.head())
    print(df_salarys.head())


    # sns.barplot(data=df, x='c1', y='c2')
    # plt.show()
    # return df_skills, df_salary



if __name__ == '__main__':

    # vacancies = get_all_vacancies()
    #
    # key_skills, description_skills, basic_skills = collect_data_skills(vacancies)
    #
    # print(f'Всего вакансий: {len(vacancies)}')
    #
    # print_collect_data_skills(basic_skills)

    create_dataframe_from_vacancy()
