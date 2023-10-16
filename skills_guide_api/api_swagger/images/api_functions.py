from http import HTTPStatus
import zipfile
from pathlib import Path

from flask import send_file

from ... import app
from ...utils.common import exists_and_makedir

static = app.config['STATIC_FOLDER']
review = static / 'review'
exists_and_makedir(review)


def create_zip():
    zipf = static / 'data.zip'
    with zipfile.ZipFile(zipf, 'w', zipfile.ZIP_DEFLATED) as zzip:
        for f in [jpg_file for jpg_file in Path(review).glob('*.jpg')]:
            zzip.write(f, arcname=f.name)
    return zipf


def get_images():
    return send_file(create_zip(), mimetype='application/zip', as_attachment=True)
