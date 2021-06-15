import copy
import json

from flask import request
from flask_restx import Resource, Namespace, fields
from model.redis.worker import Server

from common.utils import Utils
from setting.code import ReqMsg, ReqCode
import logging

worker_server = Namespace(
    name='WORKER_SERVER',
    description='WORKER TCP SERVER API'
)


@worker_server.route('/register')
class WorkerServerRegister(Resource):
    req_worker_server_register_model = worker_server.model('req_worker_server_register_model', {
        'token': fields.String(description='Access Token Value', required=True, example='Access Token Value'),
        'uid': fields.String(description='Server Key Value', required=True, example='Server Key Value')
    })

    res_worker_server_register_success_model = worker_server.model('res_worker_server_register_success_model', {
        'result': fields.String(description='result boolean', example='True')
    })

    res_worker_server_register_fail_model = worker_server.model('res_worker_server_register_fail_model', {
        'result': fields.String(description='result boolean', example='False'),
        'msg': fields.String(description='Error Message'),
        'code': fields.String(description='Error Code')
    })

    @worker_server.expect(req_worker_server_register_model)
    @worker_server.response(200, "Success", res_worker_server_register_success_model)
    @worker_server.response(400, "Fail", res_worker_server_register_fail_model)
    def post(self):
        ''' Register Worker TCP Server '''
        code = 400
        try:
            req = request.json
            chkKey = ['token', 'uid']

            if not Utils.isDicHasKey(req, chkKey):
                res = {'msg': ReqMsg.NOT_KEY, 'code': ReqCode.NOT_KEY}
                return res, code

            if not Utils.isDicKeyValueNull(req, chkKey):
                res = {'msg': ReqMsg.NOT_VALUE, 'code': ReqCode.NOT_VALUE}
                return res, code

            if 'HTTP_X_FORWARDED_FOR' in request.environ:
                ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
            elif 'REMOTE_ADDR' in request.environ:
                ip = request.list_storage_class([request.environ['REMOTE_ADDR']])[0]

            result = Server().check(ip, req['uid'])
            res = {'result': result}
            code = 200
        except Exception as ex:
            res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
        return res, code


@worker_server.route('/delete')
class WorkerServerDelete(Resource):
    req_worker_server_delete_model = worker_server.model('req_worker_server_delete_model', {
        'token': fields.String(description='Access Token Value', required=True, example='Access Token Value'),
        'ip': fields.String(description='Registered server IP', required=True, example='Registered server IP')
    })

    res_worker_server_delete_success_model = worker_server.model('res_worker_server_delete_success_model', {
        'result': fields.String(description='result boolean', example='True')
    })

    res_worker_server_delete_fail_model = worker_server.model('res_worker_server_delete_fail_model', {
        'result': fields.String(description='result boolean', example='False'),
        'msg': fields.String(description='Error Message'),
        'code': fields.String(description='Error Code')
    })

    @worker_server.expect(req_worker_server_delete_model)
    @worker_server.response(200, "Success", res_worker_server_delete_success_model)
    @worker_server.response(400, "Fail", res_worker_server_delete_fail_model)
    def post(self):
        """ Remove Registered TCP Server """
        code = 400
        try:
            req = request.json
            chkKey = ['token', 'ip']

            if not Utils.isDicHasKey(req, chkKey):
                res = {'msg': ReqMsg.NOT_KEY, 'code': ReqCode.NOT_KEY}
                return res, code

            if not Utils.isDicKeyValueNull(req, chkKey):
                res = {'msg': ReqMsg.NOT_VALUE, 'code': ReqCode.NOT_VALUE}
                return res, code

            result = Server().delete(req['ip'])
            res = {'result': result}
            code = 200
        except Exception as ex:
            res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
        return res, code  # ,header{"hi": "hello"}


@worker_server.route('/list')
class WorkerServerList(Resource):
    req_worker_server_list_model = worker_server.model('req_worker_server_list_model', {
        'token': fields.String(description='Access Token Value', required=True, example='Access Token Value')
    })

    res_worker_server_list_success_model = worker_server.model('res_worker_server_list_success_model', {
        'server': fields.String(description='server ip list', example=["xxx.xxx.xxx.xxx", "xxx.xxx.xxx.xxx"])
    })

    res_worker_server_list_fail_model = worker_server.model('res_worker_server_list_fail_model', {
        'result': fields.String(description='result boolean', example='False'),
        'msg': fields.String(description='Error Message'),
        'code': fields.String(description='Error Code')
    })

    @worker_server.expect(req_worker_server_list_model)
    @worker_server.response(200, "Success", res_worker_server_list_success_model)
    @worker_server.response(400, "Fail", res_worker_server_list_fail_model)
    def post(self):
        """ Connected Worker Server IP Information """
        code = 400
        try:
            req = request.json
            chkKey = ['token']
            if not Utils.isDicHasKey(req, chkKey):
                res = {'msg': ReqMsg.NOT_KEY, 'code': ReqCode.NOT_KEY}
                return res, code

            if not Utils.isDicKeyValueNull(req, chkKey):
                res = {'msg': ReqMsg.NOT_VALUE, 'code': ReqCode.NOT_VALUE}
                return res, code

            data = Server().list()
            res = {'server': data}
            code = 200
        except Exception as ex:
            res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
        return res, code  # ,header{"hi": "hello"}



