# controller
# -*- coding: utf-8 -*-
import logging
import datetime
import time
import os
import re
import json
import base64
import copy
from configparser import ConfigParser
from werkzeug import secure_filename
from exceptions import BadRequestException
from urllib.parse import quote
import config
import const
import common
import utils

log = logging.getLogger(__name__)


class FlaskServiceWorker(object):

    admin_type = common.get_admin_type()

    def post_method(self, params):
        return params

    def get_method(self, id):
        return id




flask_service_worker = FlaskServiceWorker()
