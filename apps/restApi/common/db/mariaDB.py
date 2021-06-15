#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import pymysql
from setting.config import config

#싱글톤 패턴으로 단 한번의 DB 커넥션을 가진다.
class MariaDB:
    _instance = None
    _dbConn = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(cls):
        if not cls._dbConn:
            # DB 연결
            cls._dbConn = pymysql.connect(
                host=config.MARIA_HOST, # 호스트 정보
                user=config.MARIA_USER, # 계정 정보
                password=config.MARIA_PWD, # 패스워드 정보
                port=config.MARIA_PORT,
                db=config.MARIA_DB, # db 정보
                charset="utf8", # 문자열 정보
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor
            )
        else:
            cls._dbConn.ping(True)
        return cls._dbConn

    def close(cls):
        if cls._dbConn:
            cls._dbConn.close();
