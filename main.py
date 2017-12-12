# -*- coding: utf-8 -*-

import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import options

from config.config import init_config
from config.settings import TEMPLATE_DIR, BASE_DIR, DEV_ENV
from urls import handlers

from utils.ioloop import IOLoop


# 设置静态文件目录
settings = dict(
    template_path=TEMPLATE_DIR,
    static_path=os.path.join(BASE_DIR, "static"),

)


# 创建Application实例，加入handlers urls
class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **settings)


# 启动信息
def run(port):
    print """
Tornado is running at http://localhost:{0}/. Press Ctrl+C to stop.
    """.format(port)


def main():
    # 读取设置
    init_config()
    options.parse_config_file('config/webssh.conf')

    # 启动一个实例
    http_server = tornado.httpserver.HTTPServer(Application())
    # 监听端口
    if not DEV_ENV:
        # 使用0.0.0.0
        http_server.listen(options.port, address="0.0.0.0")
    else:
        # 使用 127.0.0.1
        http_server.listen(options.port)
    # 异步程序
    IOLoop.instance().start()
    # 启动信息
    run(options.port)
    # 监听端口
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()