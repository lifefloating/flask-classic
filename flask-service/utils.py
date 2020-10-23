# -*- coding: utf-8 -*-
import logging
import threading
import uuid
from schematics.exceptions import ModelConversionError, ModelValidationError
from functools import wraps
import requests
from flask import jsonify, make_response, g
from const import SUCCESS, HTTP_OK
import const
from exceptions import (HttpException, UnauthorizedException,
                        AccessDeniedException, SQLException,
                        BadRequestException)

from common import json_response, failReturn
import config
import bcrypt
import re
import syslog

import traceback

log = logging.getLogger(__name__)

uuid_lock = threading.Lock()



def set_password(password):
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt(10))

def check_password(hash, pwd, default_account=False):

    password = pwd.encode('utf-8')
    hash = hash.encode('utf-8')

    if login_default_account:
        return True

    if redis_server_user.get(hash) == password:
        return True
    else:
        if bcrypt.checkpw(password, hash):
            redis_server_user.set(hash, password, 15 * 24 * 3600)
            return True
        else:
            return False


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def lower_keys(x):
    if isinstance(x, list):
        return [lower_keys(v) for v in x]
    elif isinstance(x, dict):
        return dict((k.lower(), lower_keys(v)) for k, v in x.items())
    else:
        return x


def generate_uuid():
    """Generates uuid with date and mac
    """
    global uuid_lock
    with uuid_lock:
        new_uuid = uuid.uuid4()

    return new_uuid


def exception_decorate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
                ModelConversionError,
                ModelValidationError,
        ) as e:
            log.error(f"model error info {e}")
            data = jsonify(
                falseReturn(status='INVALID_PARAMETERS', message=f"{e}"))
            response = make_response(data)
            response.status_code = 400
            return response

        except SQLException as e:
            log.error(f"SQL error info {e.message}")
            data = jsonify(
                falseReturn(status='SQL_ERROR', message=f"{e.message}"))
            response = make_response(data)
            response.status_code = e.status_code
            return response

        except UnauthorizedException as e:
            log.error(f"unauthoriztion error info {e.message}")
            data = jsonify(falseReturn(e.status, e.message))
            response = make_response(data)
            response.status_code = e.status_code
            return response

        except AccessDeniedException as e:
            log.error(f"access denied error info {e.message}")
            data = jsonify(falseReturn(e.status, e.message))
            response = make_response(data)
            response.status_code = e.status_code
            return response

        except HttpException as e:
            log.error(f"other error info {e.message}")
            data = jsonify(falseReturn(e.status, e.message))
            response = make_response(data)
            response.status_code = e.status_code
            return response

        except Exception as e:
            traceback.print_exc()
            log.error(f"system error info {e}")
            data = jsonify(falseReturn(status='SERVER_ERROR', message=f"{e}"))
            response = make_response(data)
            response.status_code = 500
            return response

    return wrapper


def wrap_resp(func):
    @wraps(func)
    @exception_decorate
    def wrap_decorator(*args, **kwargs):
        resp = func(*args, **kwargs)
        response = make_response(json_response(resp))
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        return response

    return wrap_decorator


def convert_list_to_str(list_data, obj_type=str):
    """Covert int list to str joined by ','

    :param list_data: list to convert
    :param obj_type: specify type of list object
    :return: str data
    """
    if list_data:
        if obj_type is int:
            return ','.join(str(d) for d in sorted(set(list_data)))
        elif obj_type is str:
            return ','.join(d for d in sorted(set(list_data)))
    return ''


def convert_str_to_list(string, obj_type=str):
    """Convert str data joined by ',' to list

    :param string: string to convert
    :param obj_type: specify type of list object
    :return: list data
    """
    if string:
        if obj_type is int:
            return list(map(int, string.split(',')))
        elif obj_type is str:
            return string.split(',')
    return []