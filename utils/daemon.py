# -*- coding: utf-8 -*-

import paramiko
from paramiko.ssh_exception import SSHException
from tornado.websocket import WebSocketClosedError

from ioloop import IOLoop
from utils import get_keygen

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


class Bridge(object):
    def __init__(self, websocket):
        self._websocket = websocket
        self._shell = None
        self._id = 0
        self.ssh = paramiko.SSHClient()

    @property
    def id(self):
        return self._id

    @property
    def websocket(self):
        return self._websocket

    @property
    def shell(self):
        return self._shell

    def privateKey(self, _PRIVSTE_KEY, _PRIVATE_KET_PWD):
        try:
            pkey = paramiko.RSAKey.from_private_key(StringIO(_PRIVSTE_KEY))
        except paramiko.SSHException as e:
            print e
            pkey = paramiko.DSSKey.from_private_key(StringIO(_PRIVSTE_KEY))
        return pkey

    def open(self, data={}):
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )
        try:
            self.ssh.connect(
                hostname=data["host"],
                port=int(data["port"]),
                username=(data["username"]),
                pkey=self.privateKey(get_keygen(), None)  # 获取ssh key
            )

        except SSHException as e:
            print e
            raise Exception("Could Not Connect To Host: {0}:{1}".format(data["hostname"], data["port"]))

        self.establish()

    def establish(self, term="xterm"):
        self._shell = self.ssh.invoke_shell(term)
        self._shell.setblocking(0)
        self._id = self._shell.fileno()
        IOLoop.instance().register(self)
        IOLoop.instance().add_future(self.trans_back())

    def trans_forward(self, data=""):
        if self._shell:
            self._shell.send(data)

    def trans_back(self):
        yield self.id
        connected = True
        while connected:
            try:
                result = yield
                if self._websocket:
                    try:
                        self._websocket.write_message(result)
                        # result 可获得发送和接收的数据
                    except WebSocketClosedError:
                        connected = False
                    if result.strip == 'logout':
                        connected = False
            except Exception as e:
                print e
        self.destroy()

    def destroy(self):
        self._websocket.close()
        self.ssh.close()
