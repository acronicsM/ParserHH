from http import HTTPStatus


from .sql_queries import new_user, find_by_username_query, all_users_query
from . import create_jwt_tokens


def user_registration(username, password, role_id=None, **kwargs):
    if find_by_username_query(username).first():
        return {'message': f'User {username} already exists'}, HTTPStatus.CONFLICT

    user = new_user(username=username, password=password, role_id=role_id)

    if not user:
        return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {
        'message': f'User {username} was created',
        'tokens': create_jwt_tokens(user_id=user.id, role_id=user.role_id),
    }, HTTPStatus.OK


def user_login(username, password, **kwargs):
    current_user = find_by_username_query(username).first()
    if not current_user:
        return {'message': f'User {username} doesn\'t  exists'}, HTTPStatus.UNAUTHORIZED

    if current_user.check_password(password):

        return {
            'message': f'Logged in as {current_user.username}',
            'tokens': create_jwt_tokens(user_id=current_user.id, role_id=current_user.role_id),
        }, HTTPStatus.OK
    else:
        return {'message': 'Wrong credentials'}, HTTPStatus.UNAUTHORIZED


def get_all_users():
    return {'users': [i.to_dict() for i in all_users_query().all()]}, HTTPStatus.OK
