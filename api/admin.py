from tornado.concurrent import run_on_executor
from .base import BaseHandler
import datetime
import traceback
import json

from models.admin import Admin


class LoginHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            # user = self.get_argument('user', None)
            # password = self.get_argument('password', None)
            json_data = self.request.body
            json_args = json.loads(json_data)
            user = json_args.get('user', None)
            password = json_args.get('password', None)

            if not user or not password:
                return self.response(code=10010, msg='登陆失败')

            admin = self.session.query(Admin).filter(Admin.user == user, Admin.password == password).first()
            if not admin:
                return self.response(code=10010, msg='账号密码不正确')
            else:
                uid = admin.id
                cookie = self.sessionmanager.set(uid, 7200)
                return self.response(code=10000, msg='登陆成功', data={'cookie': cookie})

        except Exception as e:
            self.logger.error(str(e.__traceback__.tb_lineno) + str(e))
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')
        finally:
            self.session.remove()


class LogoutHandler(BaseHandler):
    @run_on_executor
    def get(self):
        try:
            cookie = self.request.headers.get("cookie")
            self.sessionmanager.delete(cookie)
            return self.response(code=10000, msg='登出成功')
        except Exception as e:
            self.logger.error(str(e.__traceback__.tb_lineno) + str(e))
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')
