from HH_parser.common import get_all_vacancies, Vacancy, exists_and_makedir
from HH_parser.environment import IMAGE_FOLDER, GLOSSARY
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def add_skills_to_dict(vacancy: Vacancy,
                       skills_dict: list,
                       attr_name: str,
                       attr_index: int,
                       with_zero_salary: bool = False
                       ):

    skill_str, salary_str = 'skills', 'salarys'
    for i in vacancy.__getattribute__(attr_name):
        if i not in skills_dict:
            skills_dict[i] = {skill_str: [0, 0, 0], salary_str: []}
            skills_dict[i][skill_str] = [0, 0, 0]

        skills_dict[i][skill_str][attr_index] += 1

        if with_zero_salary or vacancy.salary_to > 0:
            skills_dict[i][salary_str].append(vacancy.salary_to)

        if with_zero_salary or vacancy.salary_from > 0:
            skills_dict[i][salary_str].append(vacancy.salary_from)


def get_dataframe_from_vacancy():
    skills = dict()
    for vacancy in get_all_vacancies():
        for k, v in enumerate(GLOSSARY):
            add_skills_to_dict(vacancy, skills, v, k)

    skills_list = [(skill, *value['skills']) for skill, value in skills.items()]
    salarys_list = [(skill, v) for skill, value in skills.items() for v in value['salarys']]

    df_skills = pd.DataFrame(skills_list, columns=['skill', *GLOSSARY])
    df_salarys = pd.DataFrame(salarys_list, columns=['skill', 'salary'])

    return df_skills, df_salarys


def save_images_skills(df_skills, nlargest=20):
    plt.figure(figsize=(20, 15), dpi=200)

    images = []

    exists_and_makedir(IMAGE_FOLDER)
    nlargest = 20
    for g in GLOSSARY:
        filename = fr'{IMAGE_FOLDER}\{g}_{nlargest}.jpg'
        plt.xticks(rotation=45)
        sns.barplot(data=df_skills.nlargest(nlargest, g), x='skill', y=g)
        plt.savefig(filename)
        plt.cla()
        images.append(filename)


def save_images_salary(df_skills, df_salarys, nlargest=20):
    unique_basic_skills = df_skills[df_skills['basic_skills'] > 0]['skill'].unique()
    df1 = df_salarys[df_salarys['skill'].isin(unique_basic_skills)]
    df1 = df1.groupby('skill', as_index=False)['salary'].mean()
    df1 = df1.sort_values(by='salary', ascending=False)

    exists_and_makedir(IMAGE_FOLDER)

    filename = fr'{IMAGE_FOLDER}\salary_{nlargest}.jpg'

    plt.figure(figsize=(20, 15), dpi=200)
    plt.xticks(rotation=45)
    sns.barplot(data=df1.nlargest(nlargest, 'salary'), x='skill', y='salary')
    plt.savefig(filename)

    return [filename]


def save_images():

    images = {'skills': [], 'salarys': []}

    df_skills, df_salarys = get_dataframe_from_vacancy()

    skills_images = save_images_skills(df_skills)
    salarys_images = save_images_salary(df_skills, df_salarys)

    images['skills'] = skills_images
    images['salarys'] = salarys_images

    return images


if __name__ == '__main__':

    save_images()
