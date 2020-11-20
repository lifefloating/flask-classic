from flask import Blueprint
from flask import request
from const import API_PREFIX
from controller.flask_service_worker import flask_service_worker
from utils import wrap_resp

df_web_service_app = Blueprint(
    'flask_service_app', __name__, url_prefix=API_PREFIX)


@flask_service_app.route(
    '/ping', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@wrap_resp
def ping():
    return 'hello'


@flask_service_app.router('posttest', methods=['POST'])
@wrap_resp
def post_test():
    params = request.get_json(force=True)
    return  flask_service_worker.post_method(params)

@flask_service_worker.router('gettest', methods=['GET'])
@wrap_resp
def get_test(id):
    return flask_service_worker.get_method(id)
