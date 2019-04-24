import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from settings import config
from handlers.urls import handlers
import pymysql
import redis

from tornado.options import define, options


define("port", default=8888,help='run on given port', type=int)


class Application(tornado.web.Application):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.db=pymysql.connect(**config.mysql_options)
        # sql = "insert into user (mobile, username, password) values (mobile,username,password)"
        # self.db.execute(sql)
        # self.db.close()
        self.redis=redis.Redis(
            connection_pool=redis.ConnectionPool(**config.redis_options)
        )


def main():
    #设置日志文件优先级
    # options.logging= config.log_level
    # # 日志文件存储路径
    # options.log_file_prefix= config.log_file
    tornado.options.parse_command_line()
    app = Application(handlers, **config.settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()


# import pymysql
# connection = pymysql.connect(host='localhost',
#                              port=3306,
#                              user='root',
#                              password='123456',
#                              db='itcast',
#                              charset='utf8')
#
# # 获取游标
# cursor = connection.cursor()

# 创建数据表
# effect_row = cursor.execute('''
# CREATE TABLE `users` (
#   `name` varchar(32) NOT NULL,
#   `age` int(10) unsigned NOT NULL DEFAULT '0',
#   PRIMARY KEY (`name`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8
# ''')
# sql="insert into user (mobile, username, password) values ('7493','jfskfsdfjf','fjsdljf')"
# sql2="select * from user"
# 插入数据(元组或列表)
# effect_row = cursor.execute(sql)
# print(effect_row)

# 插入数据(字典)
# info = {'name': 'fake', 'age': 15}
# effect_row = cursor.execute('INSERT INTO `users` (`name`, `age`) VALUES (%(name)s, %(age)s)', info)

# connection.commit()
# connection.close()