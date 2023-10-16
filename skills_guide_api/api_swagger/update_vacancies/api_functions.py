from http import HTTPStatus

from ... import app, db
from .sql_queries import all_queries, all_aggregators, get_query, delete_expired_vacancies, update_statistics
from .data_analysis import save_images

AGGREGATORS = app.config['AGGREGATORS']


def update_vacancies_by_query_id(query_name: str):
    return {agg.id: AGGREGATORS[agg.id]().update_vacancy(query=query_name)
            for agg in all_aggregators().all() if agg.id in AGGREGATORS}


def update_vacancies(query_id: int | None):
    if not query_id:
        if all_query := all_queries().all():
            return [update_vacancies_by_query_id(search_query.name) for search_query in all_query]
        else:
            return []
    else:
        return update_vacancies_by_query_id(get_query(query_id).name)


def update(query_id=None):
    result_update = {'error': False,
                     'new_vacancies': 0,
                     'remotely_vacancies': 0,
                     'total_pages': 0,
                     'updated_details': 0,
                     'vacancies_processed': 0}

    response = {'delete_vacancies': -1, 'result': result_update, 'update_statistics': False}

    # result = update_vacancies(query_id)
    #
    # for i_query in result:
    #     for i_agg in i_query.values():
    #         response['result']['error'] = max(response['result']['error'], i_agg['error'])
    #         response['result']['new_vacancies'] += i_agg['new_vacancies']
    #         response['result']['remotely_vacancies'] += i_agg['remotely_vacancies']
    #         response['result']['total_pages'] += i_agg['total_pages']
    #         response['result']['updated_details'] += i_agg['updated_details']
    #         response['result']['vacancies_processed'] += i_agg['vacancies_processed']
    #
    # if response['result']['error']:
    #     return response, HTTPStatus.INTERNAL_SERVER_ERROR
    #
    # delete_vacancies, deletion_error = delete_expired_vacancies()
    #
    # if deletion_error:
    #     return response, HTTPStatus.INTERNAL_SERVER_ERROR
    #
    # if update_statistics():
    #     return response, HTTPStatus.INTERNAL_SERVER_ERROR
    #
    # db.session.commit()

    update_img_analysis()

    # response['delete_vacancies'] = delete_vacancies
    # response['update_statistics'] = True

    return response, HTTPStatus.OK


def update_img_analysis():

    save_images()
