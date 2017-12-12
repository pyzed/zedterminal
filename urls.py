# -*- coding: utf-8 -*-

from handlers import *

handlers = [
    (r"/terminal/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([0-9]+)/([A-Z0-9]+)", IndexHandler),
    (r"/ws", WSHandler),
]