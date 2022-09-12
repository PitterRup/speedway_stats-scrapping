import logging
from functools import wraps
from urllib.parse import urlparse

from flask import g, request
from marshmallow import ValidationError, fields

log = logging.getLogger(__name__)


def validate_ma(cls_schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = cls_schema()
            log.info(u'Validating request para by schema={}'.format(schema))
            para = request.values or request.json
            try:
                result = schema.load(para)
                g.req_para = result
                return func(*args, **kwargs)
            except ValidationError as e:
                log.error(u'Incorrect requests parameters, para={}'.format(para))
                return {'message': u'Incorrect request parameters', 'errors': e.messages}, 401
        return wrapper
    return decorator


def validate_url(url):
    o = urlparse(url)
    if not o.scheme or not o.netloc:
        raise ValidationError(u'Incorrect URL address')


def opt_url():
    return fields.String(validate=validate_url)


def req_url():
    return fields.String(required=True, validate=validate_url)


def req_int():
    return fields.Integer(required=True)


def opt_int():
    return fields.Integer()
