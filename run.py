from my_api import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    host = None if app.config['ENV'] == 'development' else '0.0.0.0'
    debug = app.config['DEBUG']

    app.run(debug=debug, host=host)


# TODO: JWT SWAGGER logging
