import config.setting
from tornado.options import options
import redis
import time
import jwt
import random


class SessionManager(object):
    __instance = None

    def __init__(self, host, port, password):
        pool = redis.ConnectionPool(host=host, port=port, password=password)
        self.r = redis.Redis(connection_pool=pool)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def set(self, uid, expire_time):
        cookie = self._create_cookie(uid)
        self.r.setex(cookie, expire_time, 1)
        return cookie

    def settime(self, session_id, expire_time):
        self.r.setex(session_id, expire_time, 1)
        return

    def get(self, session_id):
        status = self.r.get(session_id)
        if status:
            return True
        else:
            return False

    def delete(self, session_id):
        self.r.delete(session_id)
        return

    def _create_cookie(self, uid):
        string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        s = ''
        for _ in range(6):
            s += string[random.randint(0, 61)]
        data = {
            'uid': uid,
            'timestamp': int(time.time()),
            'str': s
        }
        return jwt.encode(data, options.session_key).decode()
