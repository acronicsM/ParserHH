from loaders.api_loader import pages_loader, update_detail
# from loaders.dump_loader import pages_loader, update_detail
from common import get_vacancy_for_update_bin


if __name__ == '__main__':

    query = 'Python junior'

    vac_processed, total_vac = pages_loader(query_vac=query, logging=True, do_dump=True)
    print(f'Получено {vac_processed} вакансия из {total_vac}')

    update_detail(vacancies=get_vacancy_for_update_bin(), logging=True, do_dump=True)
