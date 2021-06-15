#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-


class ReqMsg:
    NOT_KEY = 'Invalid input value.'
    NOT_VALUE = 'Required value input error'
    NOT_TOKEN = 'API permission does not exist.'
    UNKNOWN = 'Unknown error occurred Please contact your system administrator.'
    SIGNIN_NOT_MATCH = 'Please check your email or password'
    SIGNIN_NOT_EMAIL = 'Please check your email or password'
    DISABLE_SESSION = 'This session has expired'

class ReqCode:
    NOT_KEY = 'C00001'
    NOT_VALUE = 'C00002'
    NOT_TOKEN = 'C00003'
    UNKNOWN = 'C00004'
    SIGNIN_NOT_MATCH = 'S00001'
    SIGNIN_NOT_EMAIL = 'S00002'
    DISABLE_SESSION = 'L00001'



