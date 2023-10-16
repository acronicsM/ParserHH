from http import HTTPStatus

from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from .api_functions import user_registration, user_login, get_all_users
from .api_model import ns, post_model_user_auth
from . import create_jwt_access_token
from ...utils.common import only_admins


@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
@ns.route('/registration')
class UserRegistration(Resource):
    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.response(int(HTTPStatus.CONFLICT), 'User already exists.')
    @ns.expect(post_model_user_auth)
    @ns.doc(description="Регистрация нового пользователя")
    def post(self):
        """ Регистрация нового пользователя """
        kwargs = post_model_user_auth.parse_args()
        return user_registration(**kwargs)


@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
@ns.route('/login')
class UserLogin(Resource):
    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.response(int(HTTPStatus.UNAUTHORIZED), 'Unauthorized.')
    @ns.expect(post_model_user_auth)
    @ns.doc(description="Авторизация пользователя")
    def post(self):
        """ Авторизация пользователя """
        kwargs = post_model_user_auth.parse_args()

        return user_login(**kwargs)


@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
@ns.route('/token/refresh')
class TokenRefresh(Resource):

    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.doc(description="Обновление токена")
    @jwt_required(refresh=True)
    def post(self):
        """ Обновление access токена """
        return {'access_token': create_jwt_access_token(get_jwt_identity())}


@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
@ns.route('/users')
class AllUsers(Resource):
    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.doc(description="Список всех пользователей")
    @jwt_required()
    @only_admins
    def get(self):
        """ Все пользователи"""
        return get_all_users()
