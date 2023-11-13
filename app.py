from skills_guide_api import app, db


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

    host = None if app.config['ENV'] == 'development' else '0.0.0.0'
    debug = app.config['DEBUG']

    app.run(debug=debug, host=host)
