from http import HTTPStatus

from flask_restx import Resource

from .api_functions import user_registration, user_login, get_all_users, del_all_users
from .api_model import ns, post_model_user_auth


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
@ns.route('/logout/access')
class UserLogoutAccess(Resource):
    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.doc(description="Регистрация нового пользователя")
    def post(self):
        return {'message': 'User logout'}


@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
@ns.route('/logout/refresh')
class UserLogoutRefresh(Resource):
    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.doc(description="Регистрация нового пользователя")
    def post(self):
        return {'message': 'User logout'}


@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
@ns.route('/token/refresh')
class TokenRefresh(Resource):
    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.doc(description="Обновление токена")
    def post(self):
        return {'message': 'Token refresh'}


@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
@ns.route('/users')
class AllUsers(Resource):
    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.doc(description="Список всех пользователей")
    def get(self):
        return get_all_users()

    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.doc(description="Удаление всех пользователей")
    def delete(self):
        return del_all_users()


@ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
@ns.route('/secret')
class SecretResource(Resource):
    @ns.response(int(HTTPStatus.OK), 'ОК.')
    @ns.doc(description="Возвращает новый секрет")
    def get(self):
        return {
            'answer': 42
        }
