import config.setting
from tornado.options import options
import redis
import time
import jwt


class SessionManager(object):
    def __init__(self, host, port, password):
        pool = redis.ConnectionPool(host=host, port=port, password=password)
        self.r = redis.Redis(connection_pool=pool)

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
        data = {
            'uid': uid,
            'timestamp': int(time.time()),
        }
        return jwt.encode(data, options.session_key).decode()
