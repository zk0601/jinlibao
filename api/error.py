import tornado.web
from tornado.escape import json_encode

class NotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        result = {"state": "0000", "msg": "This page ``{}``is not Found".format(self.request.path), "data": {}}
        self.write(json_encode(result))

    def post(self):
        result = {"state": "0000", "msg": "This page ``{}``is not Found".format(self.request.path), "data": {}}
        self.write(json_encode(result))

    def put(self):
        result = {"state": "0000", "msg": "This page ``{}``is not Found".format(self.request.path), "data": {}}
        self.write(json_encode(result))

    def delete(self):
        result = {"state": "0000", "msg": "This page ``{}``is not Found".format(self.request.path), "data": {}}
        self.write(json_encode(result))

    def head(self):
        result = {"state": "0000", "msg": "This page ``{}``is not Found".format(self.request.path), "data": {}}
        self.write(json_encode(result))

    def patch(self):
        result = {"state": "0000", "msg": "This page ``{}``is not Found".format(self.request.path), "data": {}}
        self.write(json_encode(result))
