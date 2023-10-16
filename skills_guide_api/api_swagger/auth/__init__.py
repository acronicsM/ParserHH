from pathlib import Path
from os import environ
from dotenv import load_dotenv
from skills_guide_api import app
from flask_jwt_extended import create_access_token, create_refresh_token

basedir = Path(__file__).parents[0]
load_dotenv(basedir / '.env')

model_name = __name__[__name__.rfind('.') + 1:]

description = 'Авторизация'

app.config['KEY_ROLES'] = {environ.get('KEY_ROLE_ADMIN', default='8ba12641a0ba50c4b86006c6'): 'admin',
             'user': 'user'}


def create_jwt_tokens(user_id: int, role_id: str):
    jwt_data = {'user_id': user_id, 'role': role_id}

    return {'access_token': create_jwt_access_token(jwt_data),
            'refresh_token': create_refresh_token(identity=jwt_data)}


def create_jwt_access_token(jwt_data: dict):
    return create_access_token(identity=jwt_data)