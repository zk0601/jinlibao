import jwt
import time
import tornado.web
import datetime
import config.setting
import json
from urllib.parse import urlparse
from tornado.options import options
from tornado.escape import json_encode
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class BaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(options.max_workers)

    def initialize(self):
        self.set_status(200)
        self.set_header("Content-Type", 'application/json')
        origin = self.request.headers.get("Origin")
        self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header('Access-Control-Allow-Methods', "POST, GET")
        self.set_header("Access-Control-Allow-Credentials", "true")

    @property
    def session(self):
        return self.application.session

    @property
    def basedir(self):
        return self.application.baseDir

    @property
    def requestlogger(self):
        return self.application.requestlogger

    @property
    def logger(self):
        return self.application.logger

    @property
    def sessionmanager(self):
        return self.application.sessionmanager

    def on_finish(self):
        self.session.remove()

    def on_connection_close(self):
        tornado.web.RequestHandler.on_connection_close(self)
        if self.get_status() >= 500:
            self.session.remove()

    # def encode(self, userId, openid):
    #     """
    #     根据id 生成token
    #     :param userId: 用户id
    #     """
    #     data = {"user_id": userId, "openid": openid,  "loginTime": str(datetime.datetime.now())}
    #     return jwt.encode(data, options.secret, algorithm='HS256').decode()
    #
    # def decode(self, token):
    #     """
    #     解锁token内信息
    #     :param token:
    #     """
    #     try:
    #         return jwt.decode(token,  options.secret)
    #     except:
    #         raise tornado.web.HTTPError(401)

    def response(self, data=None, code=0, msg=""):
        """
        API 统一返回格式
        :param data: 数据
        :param code: 状态码
        :param msg: 提示消息
        """
        if data is None:
            data = {}
        result = {"state": code, "msg": msg, "data": data}
        return self.write(json_encode(result))

    @run_on_executor
    def prepare(self):

        self.request_log()

        urlobj = urlparse(self.request.uri)
        request_path = urlobj.path

        if request_path in ["/admin/login", "/admin/auth"]:
            return

        # cookie = self.request.headers.get("cookie")
        cookie = self.get_cookie('JNB_cookie')
        if not cookie:
            return self.redirect("/admin/auth")
            # return self.response(code=10010, msg='非登录用户无权限')
        r = self.sessionmanager.get(cookie)
        if not r:
            return self.redirect("/admin/auth")
            # return self.response(code=10010, msg='非登录用户无权限')
        else:
            self.sessionmanager.settime(cookie, 7200)

        # token = self.request.headers.get("Authentication")
        # token = self.get_argument("token", None)
        # 登录权限
        # if request_path in self.application.Need_Token_URLs and not self.userAuthCheck(token):
        #     return self.redirect("/v1/user/auth")

    def request_log(self):
        # 输出请求日志
        paramStr = ""

        urlobj = urlparse(self.request.uri)
        request_path = urlobj.path

        json_data = self.request.body
        if not json_data:
            json_args = {}
        else:
            json_args = json.loads(json_data)
        for key, val in sorted(json_args.items()):
            if key == 'sign':
                continue
            paramStr += "%s=%s&" % (key, val)

        version = self.request.headers.get("Version", None)
        device_type = self.request.headers.get("x-dvtype", None)
        device_identity = self.request.headers.get("Device_identity", None)
        client_timestamp = self.request.headers.get("timestamp", None)
        user_agent = self.request.headers["User-Agent"]

        self.requestlogger.info("REQUEST:\tserver_timestamp=[%s], user_agent=[%s], path=[%s], params=[%s], ip=[%s], version=[%s], device_type=[%s], device_identity=[%s], client_timestamp=[%s]",
                                int(time.time())*1000, user_agent, request_path, paramStr, self.request.remote_ip, version, device_type, device_identity, client_timestamp)

    # def userAuthCheck(self, token):
    #     if not token:
    #         return False
    #
    #     arguments = self.request.arguments
    #     value = arguments['openid'][0].decode()
    #
    #     json_data = self.decode(token)
    #     if "openid" not in json_data:
    #         return False
    #     token_openid = json_data["openid"]
    #
    #     if value == token_openid:
    #         return True
    #     else:
    #         return False
