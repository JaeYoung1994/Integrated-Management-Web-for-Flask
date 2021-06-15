import copy

from flask import request
from flask_restx import Resource, Namespace, fields
from model.redis.worker import Client

from common.utils import Utils
from setting.code import ReqMsg, ReqCode

worker_client = Namespace(
    name='WORKER_CLIENT',
    description='WORKER TCP SERVER API'
)


@worker_client.route('/list')
class WorkerClientList(Resource):
    req_worker_client_list_model = worker_client.model('req_worker_client_list_model', {
        'token': fields.String(description='Access Token Value', required=True, example='Access Token Value')
    })

    res_worker_client_list_success_model = worker_client.model('res_worker_client_list_success_model', {
        'serverIP': fields.String(description='Returns a list of connected IPs for each server', example=["clientIP__1", "clientIP__2"]),
        'xxx.xxx.xxx.xxx': fields.String(example=["xxx.xxx.xxx.xxx", "xxx.xxx.xxx.xxx"])
    })

    res_worker_client_list_fail_model = worker_client.model('res_worker_client_list_fail_model', {
        'result': fields.String(description='result boolean', example='False'),
        'msg': fields.String(description='Error Message'),
        'code': fields.String(description='Error Code')
    })

    @worker_client.expect(req_worker_client_list_model)
    @worker_client.response(200, "Success", res_worker_client_list_success_model)
    @worker_client.response(400, "Fail", res_worker_client_list_fail_model)
    def post(self):
        """ Connected Client IP Information """
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

            res = Client().list()
            code = 200
        except Exception as ex:
            res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
        return res, code  # ,header{"hi": "hello"}
# class Worker_Client_List(Resource):
#     req_worker_server_register_model = worker_server.model('req_worker_server_register_model', {
#         'token': fields.String(description='Access Token Value', required=True, example='Access Token Value'),
#         'uid': fields.String(description='Server Key Value', required=True, example='Server Key Value')
#     })
#
#     res_worker_server_register_success_model = worker_server.model('res_worker_server_register_success_model', {
#         'result': fields.String(description='result boolean', example='True')
#     })
#
#     res_worker_server_register_fail_model = worker_server.model('res_worker_server_register_fail_model', {
#         'result': fields.String(description='result boolean', example='False'),
#         'msg': fields.String(description='Error Message'),
#         'code': fields.String(description='Error Code')
#     })

#     def post(self):
#         """ Check for duplicate emails in API """
#         code = 200
#         try:
#             req = request.json
#             clientRedis = ClientRedis()
#             clients = clientRedis.getClient()
#             rv = { "result":True, "data":clients}
#         except Exception as ex:
#             rv = copy.deepcopy(CommonCode.UnknownError.value)
#             rv["msg"] = str(ex)
#             code = 400
#         return rv, code  # ,header{"hi": "hello"}

# @worker_client.route('/sync/clients')
# class worker_client_sync_clients(Resource):
#     def post(self):
#         """ Check for duplicate emails in API """
#         code = 200
#         try:
#             req = request.json
#             rvKey = ['data']
#             isKey = Utils.isDicHasKey(req, rvKey)
#             if not isKey:
#                 return ReqCode.notKey.value, 400
#
#             if 'HTTP_X_FORWARDED_FOR' in request.environ:
#                 commandIp = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
#             elif 'REMOTE_ADDR' in request.environ:
#                 commandIp = request.list_storage_class([request.environ['REMOTE_ADDR']])[0]
#
#             clientRedis = ClientRedis()
#
#             clients = clientRedis.getClient()
#             connectList = []
#             for client in clients:
#                 if clients[client] == commandIp:
#                     connectList.append(client)
#
#             for conncetIp in connectList:
#                 if conncetIp not in req['data']:
#                     clientRedis.deleteClient(conncetIp)
#
#             for clientIp in req['data']:
#                 clientRedis.registClient(commandIp, clientIp)
#             rv = { "result":True }
#         except Exception as ex:
#             rv = copy.deepcopy(CommonCode.UnknownError.value)
#             rv["msg"] = str(ex)
#             code = 400
#         return rv, code  # ,header{"hi": "hello"}
#

#
# @ra_worker_client.route('/sync/clients/device')
# class worker_client_sync_device(Resource):
#     def post(self):
#         """ Check for duplicate emails in API """
#         code = 200
#         try:
#             # 값 존재 여부 확인
#             req = request.json
#             rvKey = ['ip', 'data']
#             isKey, isVal = Utils.isDicHasKey(req, rvKey), Utils.isDicKeyValueNull(req, rvKey)
#             if not isKey:
#                 return ReqCode.notKey.value, 400
#             if not isVal:
#                 return ReqCode.keyValNull.value, 400
#
#             clientRedis = ClientRedis()
#             clientRedis.registClientDevice(req['ip'], req['data'])
#             rv = CommonCode.Success.value
#         except Exception as ex:
#             rv = copy.deepcopy(CommonCode.UnknownError.value)
#             rv["msg"] = str(ex)
#             code = 400
#         return rv, code  # ,header{"hi": "hello"}
#
# @ra_worker_client.route('/get/clients/device')
# class worker_client_get_clients_device(Resource):
#     def post(self):
#         """ Check for duplicate emails in API """
#         code = 200
#         try:
#             req = request.json
#             clientRedis = ClientRedis()
#             clients = clientRedis.getClientDevice()
#             rv = {"result": True, "data": clients}
#         except Exception as ex:
#             rv = copy.deepcopy(CommonCode.UnknownError.value)
#             rv["msg"] = str(ex)
#             code = 400
#         return rv, code  # ,header{"hi": "hello"}






