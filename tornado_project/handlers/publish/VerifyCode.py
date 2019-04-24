from handlers.base.BaseHandler import BaseHandler
from libs import check_code
import io
import re



class ImageHandler(BaseHandler):
    def get(self):
        self.render('image.html')


class FistPageHandler(BaseHandler):
    def get(self):
        flag=self.get_secure_cookie('isregister')
        print(flag)
        if flag:
            mobile = self.get_secure_cookie('mobile').decode('utf8')
            cursor=self.db.cursor()
            sql="select username from user where mobile="+mobile+""
            #获取保存在cookie中的号码
            self.db.ping(reconnect=True)
            cursor.execute(sql)
            ret=cursor.fetchone()
            print(ret[0])
            self.render('has_register_first_page.html',ret=ret)
        else:
            self.render('first_page.html')

    def post(self):
        pass


class LoginHandler(BaseHandler):
    def get(self):
        # flag=self.get_secure_cookie('isregister')
        # if flag:
        #     cursor=self.db.cursor()
        #     sql="select "
        #     self.render('has_register_first_page.html')
        self.render('login.html')

    def post(self):
        da={}
        li=[]
        dic={}

        #手机号
        mobile=self.get_argument('mobile')
        #图形验证码
        imagecode=self.get_argument('imagecode')
        # 短信验证码
        messagecode=self.get_argument('messagecode')
        # 密码
        password=self.get_argument('password')
        # 确认密码
        passwordagain=self.get_argument('passwordagain')
        print(mobile,imagecode,messagecode,passwordagain,password)

        # 判断是否是手机号
        if re.match(r'1[3,4,5,7,8]\d{9}$',mobile):
            dic['mobile_info']=0
        else:
            #手机号码错误
            dic['mobile_info']=1

        # 判断图片验证码
        if imagecode.upper() == self.session['CheckCode'].upper():   # 判断用户传过来的验证码与，Session 记录的验证码是否匹配，并不区分大小写
            #图形验证码正确
            dic['imagecode_info']=0
        else:
            # 图形验证码错误
            dic['imagecode_info']=1

        # 判断手机验证码
        # if self.session['messagecode']==None:
        #     self.session['messagecode']=="1111"
        if self.session['messagecode']==messagecode:
            #手机验证码正确
            dic['messagecode_info']=0
        else:
            # 手机验证码错误
            dic['messagecode_info']=0

        #判断密码是否相同
        if password==passwordagain:
             #两次密码相符
             dic['passwd_info']=0
        else:
             #密码不相符
             dic['passwd_info']=1

        # 判断信息是否全部正确
        if dic['mobile_info']==0 and dic['imagecode_info']==0 and dic['messagecode_info']==0 and dic['passwd_info']==0:
            sql="insert into user (mobile, password) values ("+mobile+","+password+")"
            cursor=self.db.cursor()
            self.db.ping(reconnect=True)
            cursor.execute(sql)
            self.db.commit()
            self.db.close()
            li.append(dic)
            da['data']=li
            da['info']='成功'
            da['code']=200
        else:
            li.append(dic)
            da['data']=li
            da['info']='失败'
            da['code']=300

        #返回json数据
        self.write(da)


#登录
class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        #手机号
        mobile=self.get_argument('mobile')
        password=self.get_argument('password')

        #判断该用户是否已经登录
        mobile_item=self.get_secure_cookie('mobile')
        if mobile_item==None:
            mobile_item="".encode('utf8')

        if mobile==mobile_item.decode('utf8'):
            self.write({'info':1})
        else:
            cursor=self.db.cursor()
            sql="select * from user where mobile="+mobile+" and password="+password+""
            self.db.ping(reconnect=True)
            ret=cursor.execute(sql)
            print(ret)
            self.db.close()
            self.set_secure_cookie('isregister','1')
            self.set_secure_cookie('mobile',mobile)
            self.write({'info':0})




#图片验证码
class CheckImagehandler(BaseHandler):
    def get(self, *args):
        mstream = io.BytesIO()                          # 创建一个 bytes 的 io 对象（内存文件）
        img, code = check_code.create_validate_code()   # 创建图片，并写入验证码
        # img.show()
        img.save(mstream, "GIF")                        # 将图片写入到 io 对象中
        self.session["CheckCode"] = code                # 把验证码信息发送到用户对应的 Session 中，可在下次用户提交验证码时进行验证
        print(code)
        # print(mstream.getvalue())                       # 输出图片内如到 console
        self.write(mstream.getvalue())


# 手机验证码
class MobileHandler(BaseHandler):
    def post(self):
        from yunpian_python_sdk.model import constant as YC
        from yunpian_python_sdk.ypclient import YunpianClient
        import random

        # 获取手机号码
        mobile=self.get_argument('mobile')
        print(mobile)

        #生成随机四位数字
        moblie_code=''
        for x in range(4):
            moblie_code+=str(random.randint(0,9))

        # 初始化client,apikey作为所有请求的默认值
        client = YunpianClient('78ccbe77a41da6a50c3da6a67d46b489')
        param = {YC.MOBILE: mobile, YC.TEXT: '【陈华征程】您的验证码是'+moblie_code}
        r = client.sms().single_send(param)
        #保存验证码到session中
        self.session['messagecode']=moblie_code
        self.write('成功了')




