# -*- coding: utf-8 -*-

import tornado.web
import tornado.auth
import tornado.websocket

import requests
from requests import ConnectionError
from utils.daemon import Bridge
from utils.data import ClientData
from utils.utils import get_sign, get_result
from config.settings import REMOTE_URL, DEV_ENV
import time


class IndexHandler(tornado.web.RequestHandler):
    def get(self, grant_code, token, timetmp, sign):
        """
        从JAVA端获取token校验
        :param grant_code:
        :param token:
        :param time:
        :param sign:
        :return:
        """
        print grant_code, token, timetmp, sign
        verify_sign = get_sign(grant_code, token, timetmp)
        print 'verify_sign', verify_sign
        if verify_sign == sign:
            timestmp = str(time.time())[:-3]
            secret = get_sign(grant_code, token, timestmp)
            print 'secret', secret
            url = REMOTE_URL.format(grant_code, token, timestmp, secret)
            print url
            # 本地联调测试
            # url = 'https://192.168.191.1/odmc/terminal_token/verify/{0}/{1}/{2}'.format(grant_code, token, secret)
            try:
                print "外网链接"
                result = requests.post(url, verify=False, timeout=5)
                data = get_result(result)
            except ConnectionError as e:
                print 'ERROR', e
                #     result = requests.post('http://127.0.0.1:8888/', timeout=1)
                #     data = get_result(result)
                # if not data:
                print 'data is None.'
        else:
            if not DEV_ENV:
                self.send_error(403)
                return
            # 本地测试
            print "本地链接"
            data = {
                "code": 200,
                "message": 'Success',
                "data": {
                    "account": "root",
                    "hostIp": "172.16.228.134"
                }
            }
        try:
            self.set_cookie('ip', data["data"].get('hostIp', None))
            self.set_cookie('account', data["data"].get('account', None))
            self.render("index.html")
        except:
            self.send_error(status_code=404)


class WSHandler(tornado.websocket.WebSocketHandler):
    """
    websocket
    """
    clients = dict()

    def get_client(self):
        return self.clients.get(self._id(), None)

    def put_client(self):
        bridge = Bridge(self)
        self.clients[self._id()] = bridge

    def remove_client(self):
        bridge = self.get_client()
        if bridge:
            bridge.destroy()
            del self.clients[self._id()]

    @staticmethod
    def _is_init_data(data):
        return data.get_type() == 'init'

    def _id(self):
        return id(self)

    def open(self):
        self.put_client()

    def on_message(self, message):
        bridge = self.get_client()
        client_data = ClientData(message)
        if self._is_init_data(client_data):
            try:
                # 创建一个连接
                bridge.open(client_data.data)
                # todo 记录登录日志
            except Exception as e:
                print e
                self.remove_client()

        else:
            if bridge:
                # 发送命令
                bridge.trans_forward(client_data.data)
                # todo 记录命令日志

    def on_close(self):
        self.remove_client()
        # todo 记录命令日志
