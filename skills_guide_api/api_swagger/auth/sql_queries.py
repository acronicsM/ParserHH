from skills_guide_api import db
from skills_guide_api.models import Users
from skills_guide_api.utils.querys import flush


def find_by_username_query(username):
    return Users.query.filter_by(username=username)


def new_user(username, password):
    user = Users(username=username, password=Users.generate_hash(password))
    db.session.add(user)

    if not flush():
        return False

    db.session.commit()

    return True


def all_users_query():
    return Users.query


def delete_all_users_query():
    num_rows_deleted = Users.query.delete()

    if not flush():
        return False, 0

    db.session.commit()

    return True, num_rows_deleted
