from tornado.concurrent import run_on_executor
from .base import BaseHandler


class UserAuthHandler(BaseHandler):
    @run_on_executor
    def get(self):
        return self.response(code=10010, msg='非登录用户无权限')
