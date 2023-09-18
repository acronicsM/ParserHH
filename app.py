from HH_parser import app, db
from HH_parser.models import Vacancy

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

        # v = db.session.get(Vacancy, 82260854)
        # db.session.delete(v)
        # db.session.commit()

    # app.run(debug=True)
