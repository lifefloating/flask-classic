import simplejson as json
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
from const import DATE_PATTEN
import logging
import const



class LCJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Datetime class
        if isinstance(obj, datetime):
            return obj.strftime(DATE_PATTEN)
            # SQLAlchemy class
        elif isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [
                    x for x in dir(obj)
                    if not x.startswith('_') and x != 'metadata'
            ]:

                if hasattr(obj, '_fillable') and obj._fillable \
                        and field not in obj._fillable:
                    continue

                if hasattr(obj, '_hidden') and obj._hidden\
                        and field in obj._hidden:
                    continue

                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, datetime):
                        data = data.strftime(DATE_PATTEN)
                    # this will fail on non-encodable values, like other
                    # classes
                    json.dumps(data)
                    fields[field.upper()] = data
                except TypeError:
                    continue

            return fields
        return json.JSONEncoder.default(self, obj)


def json_response(data=None, status='SUCCESS'):
    resp = trueReturn(data=data, status=status)
    return LCJSONEncoder().encode(resp)


def successReturn(data=None, status='SUCCESS'):
    return {
        "status": status,
        "data": data,
        "desc": '',
    }


def failReturn(status='FAIL', message=None):
    return {
        "status": status,
        "desc": message,
        "data": False
    }