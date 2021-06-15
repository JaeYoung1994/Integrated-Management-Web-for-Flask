import json

from flask import request
from flask_restx import Resource, Namespace, fields

from model.redis.user import Session
from model.maria.sys.imw.menu import Menu

from common.utils import Utils
from setting.code import ReqMsg, ReqCode

sys_imw = Namespace(
    name='IMW 설정',
    description='IMW 프로젝트 설정 값 API'
)

@sys_imw.route('/menu')
class Sys_Imw_Menu(Resource):
    req_sys_imw_menu_model = sys_imw.model('req_sys_imw_menu_model', {
        'token': fields.String(description='Access Token Value', required=True, example='Access Token Value'),
        'session': fields.String(description='Session Value', required=True, example='Session Value')
    })

    res_sys_imw_menu_success_model = sys_imw.model('res_sys_imw_menu_success_model', {
        'data': fields.String(description='Error Message')
    })

    res_sys_imw_menu_false_model = sys_imw.model('res_sys_imw_menu_false_model', {
        'msg': fields.String(description='Error Message'),
        'code': fields.String(description='Error Code'),
    })

    @sys_imw.expect(req_sys_imw_menu_model)
    @sys_imw.response(200, "Success", res_sys_imw_menu_success_model)
    @sys_imw.response(400, "Fail", res_sys_imw_menu_false_model)
    def post(self):
        """ Check for duplicate emails in API """
        code = 400
        try:
            req = request.json
            chkKey = ['token', 'session']
            if not Utils.isDicHasKey(req, chkKey):
                res = {'msg': ReqMsg.NOT_KEY, 'code': ReqCode.NOT_KEY}
                return res, code

            if not Utils.isDicKeyValueNull(req, chkKey):
                res = {'msg': ReqMsg.NOT_VALUE, 'code': ReqCode.NOT_VALUE}
                return res, code

            reqSession = req.get('session')
            session = Session()
            account = session.getSession(reqSession)

            if not account:
                res = {'msg': ReqMsg.DISABLE_SESSION, 'code': ReqCode.DISABLE_SESSION}
                return res, code

            account = json.loads(account)

            rvMenu = Menu().getMainMenuList(account)
            if rvMenu['result']:
                res = {"data": rvMenu['data']}
            else:
                res = {}
            code = 200
        except Exception as ex:
            res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
        return res, code