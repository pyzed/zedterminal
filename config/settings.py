# -*- coding: utf-8 -*-
import os

# 环境
HOME_DIR = os.environ['HOME']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
PUBKEY_DIR = os.path.join(HOME_DIR, '.ssh/id_rsa')

# token 验证/盐值
SALT = 'ocdm2!23A'

# 获取远程JAVA数据地址
REMOTE_URL = 'http://192.168.121.210/odmc/terminal_token/verify/{0}/{1}/{2}/{3}'

# 开发环境， 如果开启 0.0.0.0 远程链接，设置成 False
DEV_ENV = True
