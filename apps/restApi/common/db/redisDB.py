#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import redis
from setting.config import config

#싱글톤 패턴으로 단 한번의 DB 커넥션을 가진다.
class RedisDB:
    _instance = None
    _dbConn = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(cls):
        if not cls._dbConn:
            # DB 연결
            cls._dbConn = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PWD,
                decode_responses=True
            )
        return cls._dbConn

    def close(cls):
        if cls._dbConn:
            cls._dbConn.close();
