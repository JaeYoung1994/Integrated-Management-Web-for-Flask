import copy
import json
import logging

from flask import request
from flask_restx import Resource, Namespace, fields

from model.maria.user import Account
from model.redis.user import Session
from common.security.encryption import Encryption
from common.utils import Utils
from setting.code import ReqMsg, ReqCode
from setting.config import config

auth = Namespace(
    name='로그인',
    description='로그인 관련 API'
)


@auth.route('/signin')
class Auth_Signin(Resource):
    auth_signin_account_model = auth.model('auth_signin_account_model', {
        'email': fields.String(description='Login Account', required=True, example='User email'),
        'password': fields.String(description='Login Account', required=True, example='User password')
    })

    req_auth_signin_model = auth.model('req_auth_signin_model', {
        'token': fields.String(description='Access Token Value', required=True, example='Access Token Value'),
        'account': fields.Nested(auth_signin_account_model)
    })

    res_auth_signin_success_model = auth.model('res_auth_signin_success_model', {
        'session': fields.String(description='Return created session value')
    })

    res_auth_signin_false_model = auth.model('res_auth_signin_false_model', {
        'msg': fields.String(description='Error Message'),
        'code': fields.String(description='Error Code')
    })

    @auth.expect(req_auth_signin_model)
    @auth.response(200, 'Success', res_auth_signin_success_model)
    @auth.response(400, 'Fail', res_auth_signin_false_model)
    def post(self):
        ''' Sign In API '''
        try:
            code = 400
            req = request.json
            chkKey = ['token', 'account']
            if not Utils.isDicHasKey(req, chkKey):
                res = {'msg': ReqMsg.NOT_KEY, 'code': ReqCode.NOT_KEY}
                return res, code

            if not Utils.isDicKeyValueNull(req, chkKey):
                res = {'msg': ReqMsg.NOT_VALUE, 'code': ReqCode.NOT_VALUE}
                return res, code

            chkKey = ['email', 'password']
            if not Utils.isDicHasKey(req['account'], chkKey):
                res = {'msg': ReqMsg.NOT_KEY, 'code': ReqCode.NOT_KEY}
                return res, code

            if not Utils.isDicKeyValueNull(req['account'], chkKey):
                res = {'msg': ReqMsg.NOT_VALUE, 'code': ReqCode.NOT_VALUE}
                return res, code

            if req['token'] != config.TOKEN:
                res = {'msg': ReqMsg.NOT_TOKEN, 'code': ReqCode.NOT_TOKEN}
                return res, code

            account = Account()
            reqAccount = req['account']
            userInfo = account.getAccountInfo(reqAccount)
            if not userInfo['result']:
                res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
                return res, code
            if userInfo['data'] is None:
                res = {'msg': ReqMsg.SIGNIN_NOT_EMAIL, 'code': ReqCode.SIGNIN_NOT_EMAIL}
                return res, code

            if not Encryption().checkBcrypt(userInfo['data']['password'], reqAccount['password']):
                res = {'msg': ReqMsg.SIGNIN_NOT_MATCH, 'code': ReqCode.SIGNIN_NOT_MATCH}
                return res, code
            else:
                user = json.dumps({'email': userInfo['data']['email']})
                userSession = Session().createSession(user, config.DUPLICATE_LOGIN)
                res = {'session': userSession}
                code = 200
        except Exception as ex:
            res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
        return res, code


@auth.route('/signout')
class Auth_Signout(Resource):
    req_auth_signout_model = auth.model('req_auth_signout_model', {
        'token': fields.String(description='Access Token Value', required=True, example='Access Token Value'),
        'session': fields.String(description='Session Value', required=True, example='Session Value')
    })

    res_auth_signout_success_model = auth.model('res_auth_signout_success_model', {
        'result': fields.String(description='return result value'),
    })

    res_auth_signout_false_model = auth.model('res_auth_signout_false_model', {
        'msg': fields.String(description='Error Message'),
        'code': fields.String(description='Error Code'),
    })

    @auth.expect(req_auth_signout_model)
    @auth.response(200, 'Success', res_auth_signout_success_model)
    @auth.response(400, 'Fail', res_auth_signout_false_model)
    def post(self):
        ''' Sign out API '''
        try:
            code = 400
            req = request.json
            chkKey = ['token', 'session']
            if not Utils.isDicHasKey(req, chkKey):
                res = {'msg': ReqMsg.NOT_KEY, 'code': ReqCode.NOT_KEY}
                return res, code

            if not Utils.isDicKeyValueNull(req, chkKey):
                res = {'msg': ReqMsg.NOT_VALUE, 'code': ReqCode.NOT_VALUE}
                return res, code

            if req['token'] != config.TOKEN:
                res = {'msg': ReqMsg.NOT_TOKEN, 'code': ReqCode.NOT_TOKEN}
                return res, code

            reqSession = req.get("session")
            Session().deleteSession(reqSession)
            res = {'result': True}
            code = 200
        except Exception as ex:
            res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
        return res, code


@auth.route('/check/session')
class Auth_Check_Session(Resource):
    req_auth_check_session_model = auth.model('req_auth_check_session_model', {
        'token': fields.String(description='Access Token Value', required=True, example='Access Token Value'),
        'session': fields.String(description='Session Value', required=True, example='Session Value')
    })

    auth_check_session_success_data_model = auth.model('auth_check_session_success_data_model', {
        'email': fields.String(description='Session owner email')
    })

    res_auth_check_session_success_model = auth.model('res_auth_check_session_success_model', {
        'data': fields.Nested(auth_check_session_success_data_model)
    })

    res_auth_check_session_false_model = auth.model('res_auth_check_session_false_model', {
        'msg': fields.String(description='Error Message'),
        'code': fields.String(description='Error Code'),
    })

    @auth.expect(req_auth_check_session_model)
    @auth.response(200, 'Success', res_auth_check_session_success_model)
    @auth.response(400, 'Fail', res_auth_check_session_false_model)
    def post(self):
        ''' Session Expiration Check API '''
        code = 400
        try:
            req = request.json
            chkKey = ['token', 'session']
            if not Utils.isDicHasKey(req, chkKey):
                res = {'msg': ReqMsg.NOT_KEY, 'code': ReqCode.NOT_KEY}
                return res, code

            if not Utils.isDicKeyValueNull(req, chkKey):
                res = {'msg': ReqMsg.NOT_VALUE, 'code': ReqCode.NOT_VALUE}
                return ReqCode.keyValNull.value, 400

            if req['token'] != config.TOKEN:
                res = {'msg': ReqMsg.NOT_TOKEN, 'code': ReqCode.NOT_TOKEN}
                return res, code

            reqSession = req.get('session')
            session = Session()
            check = session.checkSession(reqSession)
            if not check:
                rv = {'result': False, 'user': {}}
            else:
                data = session.getSession(reqSession)
                rv = {'result': True, 'user': json.loads(data)}
            code = 200
        except Exception as ex:
            res = {'msg': ReqMsg.UNKNOWN, 'code': ReqCode.UNKNOWN}
        return rv, code


