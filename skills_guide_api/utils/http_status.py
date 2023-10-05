from flask import make_response


def status_500(removal=False):
    return make_response(f' failed to {"delete" if removal else "write"} data', 500)


def status_208(id, removal=False):
    return make_response(f'an entry with id {id} {"not " if removal else ""}exists', 500)


def status_200():
    return make_response('well done', 200)


def status_400():
    return make_response('required arguments are missing', 400)


def status_405():
    return make_response('Method Not Allowed', 405)