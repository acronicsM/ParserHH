from http import HTTPStatus

from skills_guide_api.models import Users
from .sql_queries import new_user, find_by_username_query, all_users_query, delete_all_users_query


def user_registration(username, password):

    if find_by_username_query(username).first():
        return {'message': f'User {username} already exists'}, HTTPStatus.CONFLICT

    result = new_user(username=username, password=password)

    if not result:
        return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR

    return f'User {username} was created', HTTPStatus.OK


def user_login(username, password):
    current_user = find_by_username_query(username).first()
    if not current_user:
        return {'message': f'User {username} doesn\'t  exists'}, HTTPStatus.UNAUTHORIZED

    if Users.verify_hash(password, current_user.password):
        return {'message': f'Logged in as {username}'}, HTTPStatus.OK
    else:
        return {'message': 'Wrong credentials'}, HTTPStatus.UNAUTHORIZED


def get_all_users():
    return {'users': [i.to_dict() for i in all_users_query().all()]}, HTTPStatus.OK


def del_all_users():

    error, num_rows_deleted = delete_all_users_query()

    if error:
        return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {'message': f'{num_rows_deleted} row(s) deleted'}, HTTPStatus.OK
