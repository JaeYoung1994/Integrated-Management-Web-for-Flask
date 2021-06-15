#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import os
from flask import Flask
from flask_restx import Api

from setting.config import config

from app.auth.user import auth
from app.sys.imw.menu import sys_imw
from app.worker.server import worker_server
from app.worker.client import worker_client

# from app.data.user import data_user
#
# from app.worker.command.commandController import ra_worker_command
# from app.worker.client.clientController import ra_worker_client
from common.security.encryption import Encryption

def run():
    conf = config
    app = Flask(__name__)
    Encryption().setBcrypt(app)
    api = Api(
        app,
        version='dev_0.1',
        title='Integrated API Server',
        description='RestAPI for server management',
        terms_url="/",
        contact="unripedata@gmail.com",
        license="MIT",
        url_scheme='http'
    )

    api.add_namespace(auth, '/auth')
    api.add_namespace(sys_imw, '/sys/imw')
    api.add_namespace(worker_server, '/worker/server')
    api.add_namespace(worker_client, '/worker/client')

    app.run(host=conf.HOST, port=conf.PORT, debug=conf.DEBUG)




