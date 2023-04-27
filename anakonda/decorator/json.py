from functools import wraps

from flask import request

from anakonda.util import jsonify


def json_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.content_type != "application/json":
            return jsonify(status=400, code=105)
        return f(*args, **kwargs)

    return wrapper
