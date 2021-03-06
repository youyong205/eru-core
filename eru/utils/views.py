# coding: utf-8

import json
from datetime import datetime
from functools import wraps
from flask import request, abort, Response

from eru.models.base import Base
from eru.common import code


def check_request_json(keys, abort_code=code.HTTP_BAD_REQUEST, abort_msg=''):
    if not isinstance(keys, list):
        keys = [keys, ]
    def deco(function):
        @wraps(function)
        def _(*args, **kwargs):
            data = request.get_json()
            if not (data and all((k in data) for k in keys)):
                raise EruAbortException(abort_code, abort_msg)
            return function(*args, **kwargs)
        return _
    return deco


def check_request_args(keys, abort_code=code.HTTP_BAD_REQUEST, abort_msg=''):
    if not isinstance(keys, list):
        keys = [keys, ]
    def deco(function):
        @wraps(function)
        def _(*args, **kwargs):
            if not all((k in request.args) for k in keys):
                raise EruAbortException(abort_code, abort_msg)
            return function(*args, **kwargs)
        return _
    return deco


class EruJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Base):
            return obj.to_dict()
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(EruJSONEncoder, self).default(obj)


def jsonify(code=code.HTTP_OK):
    def _jsonify(f):
        @wraps(f)
        def _(*args, **kwargs):
            r = f(*args, **kwargs)
            return r and Response(json.dumps(r, cls=EruJSONEncoder), status=code, mimetype='application/json')
        return _
    return _jsonify


class EruAbortException(Exception):

    def __init__(self, code, msg=''):
        self.code = code
        self.msg = msg

