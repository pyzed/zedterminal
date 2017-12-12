# -*- coding: utf-8 -*-

from tornado.options import define


def init_config():
    define('port', default=8001, type=int, help='run on the given port')
