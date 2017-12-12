# -*- coding: utf-8 -*-

import os
import json
import sys
import hashlib
from config.settings import SALT, PUBKEY_DIR

_PLATFORM = sys.platform


class Platform(object):
    # 返回系统平台
    @staticmethod
    def detail():
        return _PLATFORM

    @staticmethod
    def is_win():
        return _PLATFORM.startswith('win')

    @staticmethod
    def is_linux():
        return _PLATFORM.startswith('linux')

    @staticmethod
    def is_mac():
        return _PLATFORM.startswith('darwin')


def get_keygen():
    """
    读取 ssh key
    :return:
    """
    with open(PUBKEY_DIR, 'r') as f:
        result = f.read()
    return result


def get_sign(grant_code, token, timestamp):
    """
    生成 md5 返回
    :param grant_code:
    :param token:
    :param timestamp:
    :return:
    """
    new_sign = grant_code + '+' + timestamp + '+' + token + '{' + SALT + '}'
    md = hashlib.md5()
    md.update(new_sign)
    return md.hexdigest().upper()


def get_result(result):
    """
    验证 Java 跳转连接 post 请求获取的数据
    :param result:dict
    :return:
    """
    content = str(result.text.encode('utf-8'))
    try:
        print content
        data = json.loads(content)
    except Exception as e:
        print 'get_result', e
        data = {}
        l = content.lstrip("'").rstrip("'").lstrip('"').rstrip('"').split('&')
        for i in l:
            a = i.split('=')
            data[a[0]] = a[1]
    return data


if __name__ == '__main__':
    # grant_code = '6955433e-4fbf-4a15-8376-313471af3b5c'
    # token = 'a95a76e2-a046-4445-9817-4b04ec30859a'
    # time = '1504150295642'
    # a = get_sign(grant_code, token, time)
    # print a

    b = get_keygen()
    print b
