# Web Terminal

一个网页终端模拟器

主要依赖：

    python 2.7.13
    tornado 4.5.2
    paramiko 2.2.1
    requests 2.18.4


## 运行

1. 安装必要的依赖库

见文件目录下的requirements.txt

目录终端下执行

```bash
pip install -r requirements.txt
```

**内网需将所有安装包下载到本地，执行`pip install <package name>`**

2. 运行main.py

```bash
python main.py
```

**外网访问：将`config/settings.py`内的`DEV_ENV = True` 改成 `DEV_ENV = False`**

## 验证说明

Java端 请求 `http://ip:8001/terminal/grant_code/token_string/TIMESTAMP/sign`

其中, `grant_code`, `token_string`, `TIMESTAMP`, `sign`为Java端生成。

`verify_sign = grant_code + '+' + TIMESTAMP + '+' + token + '{' + SALT + '}'`

如果`verify_sign == sign`，

POST请求`http://192.168.121.210/terminal_token/verify/{grantCode}/{token}/{TIMESTAMP}/{sign}`，

**注: 正式地址根据Java端提供，修改 `config/settings.py` 下 `REMOTE_URL`**

请求成功后会获取到一个json数据

```json
{
    "code":200,
    "message":"",
    "data":{
    "account":"admin",
    "hostIp":"192.168.121.218",
    "token":""
     }
}
```

如果认证失败

```json
{
    "code":500,
    "message":"参数签名异常，请重新认证！",
    "data":null
}
```

#### Example 

```
grantCode: 6955433e-4fbf-4a15-8376-313471af3b5c
token: a95a76e2-a046-4445-9817-4b04ec30859a
time: 1504150295642
apiTokenSecret: ocdm2!23A
sign: 5D28DA868C019A2EA9A1DE690E25F1FA

原始加密串是
6955433e-4fbf-4a15-8376-313471af3b5c+a95a76e2-a046-4445-9817-4b04ec30859a+1504150295642{ocdm2!23A}
md5加密结果：5D28DA868C019A2EA9A1DE690E25F1FA (所有字母大写)
```

## 其他参数 `settings.py`

    REMOTE_URL : 设置远程JAVA端地址，需要从这个地址获取主机数据
    测试为`'http://192.168.121.210/odmc/terminal_token/verify/{0}/{1}/{2}/{3}'`
    {1} 为 grant_code
    {2} 为 token
    {3} 为 TIMESTAMP
    {4} 为 sign
    
    
    DEV_ENV = True : 设置是否为开发环境
    如果部署，请设置 DEV_ENV = False
