import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import options
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
import os

import urls
import config.setting
from api.error import NotFoundHandler
from utils.log_helper import logger, request_log


class Application(tornado.web.Application):
    def __init__(self):
        self.baseDir = os.path.dirname(os.path.realpath(__file__))

        database_url = 'mysql+mysqldb://{}:{}@{}/{}?charset=utf8'.format(options.mysql_user, options.mysql_password,
                                                                         options.mysql_host, options.mysql_database)
        engine = create_engine(database_url, encoding='utf8', pool_size=options.pool_size,
                               pool_recycle=options.pool_recycle, echo=False, echo_pool=False)
        self.session = scoped_session(sessionmaker(bind=engine, autocommit=False))

        settings = {
            'debug': False,
            'default_handler_class': NotFoundHandler
        }

        super(Application, self).__init__(urls.handlers, **settings)
        # self.Need_Token_URLs = urls.Need_Token_URLs
        self.logger = logger(self.baseDir + '/logs/application.log', logging.INFO)
        self.requestlogger = request_log(self.baseDir + '/logs/requests.log', logging.INFO)


def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()


if __name__ == '__main__':
    main()
