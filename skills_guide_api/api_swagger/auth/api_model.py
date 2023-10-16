from flask_restx import Namespace, reqparse
from . import model_name, description

ns = Namespace(name=model_name, validate=True, description=description)

post_model_user_auth = reqparse.RequestParser(bundle_errors=True)
post_model_user_auth.add_argument('username',
                                  type=str,
                                  location='args',
                                  help='Логин пользователя',
                                  required=True)

post_model_user_auth.add_argument('password',
                                  type=str,
                                  location='args',
                                  help='Пароль пользователя',
                                  required=True)


post_model_user_auth.add_argument('role_id',
                                  type=str,
                                  location='args',
                                  help='Идентификатор роли пользователя. Если не указан то обычный пользователь',)

