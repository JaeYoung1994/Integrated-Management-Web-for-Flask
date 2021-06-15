#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
from common.db.redisDB import RedisDB
from uuid import uuid4


class Session(RedisDB):
    _prefix = 'imw:session:'
    _timeout = 3600

    def createSession(cls, username, duplicate=False):
        cls.connect()
        skey = str(uuid4())
        if not duplicate:
            for key in cls._dbConn.keys(cls._prefix+"*"):
                if cls._dbConn.get(key) == username:
                    cls.deleteSession(key)
        cls._dbConn.setex(cls._prefix + skey, cls._timeout, username)
        return skey

    def getSession(cls, session):
        cls.connect()
        username = {}
        session = cls._prefix + session
        sessions = cls._dbConn.keys(cls._prefix+"*")
        if session in sessions:
            username = cls._dbConn.get(session)
        return username

    def checkSession(cls, skey):
        cls.connect()
        result = False
        sessions = cls._dbConn.keys(cls._prefix + "*")
        username = cls._dbConn.get(cls._prefix + skey)
        if username is not None:
            cls._dbConn.expire(cls._prefix + skey, cls._timeout)
            result = True
        return result

    def deleteSession(cls, skey):
        cls.connect()
        cls._dbConn.delete(cls._prefix +skey)