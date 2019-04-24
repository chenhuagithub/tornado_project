import tornado.web
from libs.mysession import Session


class BaseHandler(tornado.web.RequestHandler):
    '''handler基类'''

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        pass

    def write_error(self, status_code, **kwargs):
        pass

    def set_default_headers(self):
        pass

    # handler实例化时被调用
    def initialize(self):
        self.session = Session(self)  # 通过 initialize 方法调用自定义 Session 方法

    def on_finish(self):
        pass


