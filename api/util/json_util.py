import datetime
import decimal


def json_encoder(obj):
    if isinstance(obj, datetime.datetime):
        return {
            '_tp': 'datetime',
            'value': obj.strftime('%Y-%m-%d %H:%M:%S'),
        }
    elif isinstance(obj, datetime.date):
        return {
            '_tp': 'date',
            'value': obj.strftime('%Y-%m-%d'),
        }
    elif isinstance(obj, decimal.Decimal):
        return {
            '_tp': 'decimal',
            'value': float(obj),
        }
    else:
        return obj
