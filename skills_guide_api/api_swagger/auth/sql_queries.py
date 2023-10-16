from skills_guide_api import db, app
from skills_guide_api.models import Users
from ...utils.sql_queries import flush


def find_by_username_query(username):
    return Users.query.filter_by(username=username)


def new_user(username, password, role_id=None):

    role = role_id if role_id else app.config['KEY_ROLES']['user']
    user = Users(username=username, role_id=role)
    user.set_password(password)

    db.session.add(user)

    if not flush():
        return None

    db.session.commit()

    return user


def all_users_query():
    return Users.query
