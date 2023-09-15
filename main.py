from common import get_vacancy_for_update_bin, delete_expired_vacancies
from data_analysis import save_images
from loaders.api_loader import pages_loader, update_detail
# from loaders.dump_loader import pages_loader, update_detail


if __name__ == '__main__':

    query = 'Python junior'

    pages_loader(query_vac=query, logging=True, do_dump=True)

    delete_expired_vacancies(logging=True)

    update_detail(vacancies=get_vacancy_for_update_bin(), logging=True, do_dump=True)

    save_images()


