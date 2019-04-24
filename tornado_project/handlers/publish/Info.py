from handlers.base.BaseHandler import BaseHandler
from fdfs_client.client import Fdfs_client
import os
from PIL import Image
import datetime
import time

class UserInfoHandler(BaseHandler):
    def get(self):
        self.render('user_info.html')

    def post(self):
        pass


class OneInfoHandler(BaseHandler):
    def get(self):
        self.render('one_info.html')

    def post(self):
        #获取用户名
        username=self.get_argument('username')
        #获取该用户的号码
        mobile=self.get_secure_cookie('mobile').decode('utf8')
        cursor=self.db.cursor()
        sql="update user set username='"+username+"'where mobile='"+mobile+"'"
        self.db.ping(reconnect=True)
        cursor.execute(sql)
        self.db.commit()
        self.db.close()
        self.write({'info':0})


#图片上传
class ImageUploadHandler(BaseHandler):
    # 获取图片
    def get(self):
        mobile = self.get_secure_cookie('mobile')

        print(mobile)
        if mobile:
            cursor=self.db.cursor()
            sql="select file_id,username from user where mobile='"+mobile.decode('utf8')+"'"
            self.db.ping(reconnect=True)
            cursor.execute(sql)
            ret=cursor.fetchone()
            print(ret[0])
            print(ret[1])
            self.write({'file_path':ret[0],'user':ret[1],'code':200})
        else:
            self.write({'code':300})

    def post(self):
        file=self.request.files

        #用时间生成随机字符串作为文件名，以保证文件名的唯一
        filename=time.strftime('%Y%m%d%H%M%S')+'.jpg'
        file_img=file.get('file')
        if file_img:
            # 获取图片
            img=file_img[0]['body']
            #创建一个路径存储图片
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'bufferimage/'+filename),'wb') as f:
                f.write(img)

            #配置文件路径
            client=Fdfs_client(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'fastdfs/client.conf'))
            # 把图片上传到服务器
            ret=client.upload_by_filename(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'bufferimage/'+filename))
            ip=ret['Storage IP']
            file_id=ret['Remote file_id']
            file_path='http://'+ip+'/'+file_id
            print(file_path)

            #保存图片路径
            mobile=self.get_secure_cookie('mobile').decode('utf8')
            cursor=self.db.cursor()
            sql="update user set file_id='"+file_path+"' where mobile='"+mobile+"'"
            self.db.ping(reconnect=True)
            cursor.execute(sql)
            self.db.commit()
            self.db.close()
        self.write({'info':0})


class GetUsernameMobileHandler(BaseHandler):
    def get(self):
        #从数据库中拿数据:username
        cursor=self.db.cursor()
        mobile=self.get_secure_cookie('mobile').decode('utf8')
        print(mobile)
        sql="select username from user where mobile='"+mobile+"'"
        self.db.ping(reconnect=True)
        cursor.execute(sql)
        ret=cursor.fetchone()
        print(ret[0])

        #获取号码
        mobile=self.get_secure_cookie('mobile')
        if mobile:
            pass
        else:
            mobile="".encode('utf8')

        mobile=mobile.decode('utf8')


        self.write({'username':ret[0],'mobile':mobile})



    def post(self):
        pass

# 订单
class MyOrderHandler(BaseHandler):
    def get(self):
        try:
            #从数据库中获取订单信息
            mobile=self.get_secure_cookie('mobile').decode('utf8')
            cursor=self.db.cursor()
            sql="select i.id,i.create_time,i.live_time,i.left_time,i.monney,i.order_status,i.evaluate,i.house_image_url from user left join it_order i on user.id = i.user_id where mobile='"+mobile+"'"
            self.db.ping(reconnect=True)
            cursor.execute(sql)
            ret=cursor.fetchall()
            self.db.close()

            li=[]
            for x in ret:
                lis=list(x)
                print(x[2])
                print(x[3])
                end_time=int(time.mktime(datetime.datetime.strptime(str(x[3]),'%Y-%m-%d %H:%M:%S').timetuple()))
                begin_time=int(time.mktime(datetime.datetime.strptime(str(x[2]),'%Y-%m-%d %H:%M:%S').timetuple()))
                ti=end_time-begin_time
                day=ti//86400
                print(day)
                lis.append(day+1)
                li.append(lis)
            self.render('myorder.html',ret=ret,li=li)

        except:
            self.render('myorder2.html')


    def post(self):
        pass

#实名验证
class RealNameHandler(BaseHandler):
    def get(self):
        self.render('real_name.html')

    def post(self):
        name=self.get_argument('name')
        idcode=self.get_argument('idcode')
        gender=self.get_argument('gender')

        #存储数据
        #获取游标
        cursor=self.db.cursor()
        #获取用户id
        mobile=self.get_secure_cookie('mobile').decode('utf8')
        sql_getid="select id from user where mobile='"+mobile+"'"
        self.db.ping(reconnect=True)
        cursor.execute(sql_getid)
        id=cursor.fetchone()[0]
        print(type(id))

        print(name,idcode,gender,id)
        #存储实名验证的信息
        sql="insert into it_real_name (name, idcode, gender, user_id) values ('"+name+"','"+idcode+"','"+gender+"',"+str(id)+")"
        print(sql)
        #如果连接已经断开则重新连接
        self.db.ping(reconnect=True)
        #执行sql语句
        cursor.execute(sql)
        #提交数据
        self.db.commit()
        #断开连接
        self.db.close()

        self.write({'code':200})


#判断是否已经实名验证
class IsRealNameHandler(BaseHandler):
    def get(self):
        #从数据库中查询数据，判断是否已经实名验证
        cursor=self.db.cursor()
        mobile=self.get_secure_cookie('mobile').decode('utf8')
        #使用内连接进行查询
        sql="select user.id from user inner join it_real_name irn on user.id = irn.user_id where mobile='"+mobile+"'"
        #如果数据库连接已经断开则重新连接
        self.db.ping(reconnect=True)
        cursor.execute(sql)
        ret=cursor.fetchone()
        self.db.close()
        self.render('myhouse.html',ret=ret)

    def post(self):
        #从数据库中查询数据，判断是否已经实名验证
        cursor=self.db.cursor()
        mobile=self.get_secure_cookie('mobile').decode('utf8')
        #使用内连接进行查询
        sql="select user.id from user inner join it_real_name irn on user.id = irn.user_id where mobile='"+mobile+"'"
        #如果数据库连接已经断开则重新连接
        self.db.ping(reconnect=True)
        cursor.execute(sql)
        ret=cursor.fetchone()
        self.db.close()

        if ret:
            self.write({"code":200})
        else:
            self.write({"code":300})







