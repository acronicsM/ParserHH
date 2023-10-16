from pathlib import Path
import requests
from http import HTTPStatus

from flask import jsonify
from flask_restx import abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

from skills_guide_api import app


def create_successful_response(status_code, message):
    response = jsonify(status="success", message=message)
    response.status_code = status_code
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def only_admins(func):
    def wrappers(*args, **kwargs):
        identity = get_jwt_identity()
        key_roles = app.config['KEY_ROLES']

        if 'role' in identity and identity['role'] in key_roles and key_roles[identity['role']] == 'admin':
            return func(*args, **kwargs)
        else:
            abort(HTTPStatus.UNAUTHORIZED, message="The method is not available", status="fail")
        pass

    return wrappers
