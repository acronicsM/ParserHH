from skills_guide_api import db


def flush():
    try:
        db.session.flush()
    except:
        db.session.rollback()
        return False

    return True
