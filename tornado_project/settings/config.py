import os

# Application配置文件
settings=dict(
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "statics"),
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
    debug = True,
    cookie_secret='I17mosMgQM6He6POdlUkpow7C0XWdkB0v7bFz77vab8=',
    # # 开启xsrf保护，开启这个功能时，必须开启cookie_secret
    # xsrf_cookies=True
)

# mysql
mysql_options={
    'host' : '127.0.0.1',
    'port' : 3306,
    'user' : 'root',
    'passwd' :'123456',
    'db' : 'itcast',
    'charset':'utf8'
}

# redis
redis_options={
    'host':'127.0.0.1',
    'password':''
}

#日志
# log_file=os.path.join(os.path.dirname(os.path.dirname(__file__)),'logs/log')
# log_level='debug'