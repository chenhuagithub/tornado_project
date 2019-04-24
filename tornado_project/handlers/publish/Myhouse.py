from handlers.base.BaseHandler import BaseHandler
import os
import time
from fdfs_client.client import Fdfs_client


class MyHouseHandler(BaseHandler):
    def get(self):
        try:
            mobile=self.get_secure_cookie('mobile').decode('utf8')
            cursor=self.db.cursor()
            sql="select im.id,house_name,house_image_url, location,price,create_time from user inner join it_public_house im on user.id = im.user_id where mobile='"+mobile+"'"
            self.db.ping(reconnect=True)
            cursor.execute(sql)
            ret=cursor.fetchall()
            self.render('myhouse.html',ret=ret)
        except:
            self.render('myhouse2.html')


    def post(self):
        pass


class PublicNewHouse(BaseHandler):
    def get(self):
        self.render('publicnewhouse.html')

    def post(self):
        #获取数据
        house_image_url = self.get_argument('house_image_url')
        house_name=self.get_argument('house_name')
        price=self.get_argument('price')
        location=self.get_argument('location')
        detail_addr=self.get_argument('detail_addr')
        house_amount=self.get_argument('house_amount')
        house_area=self.get_argument('house_area')
        house_account=self.get_argument('house_account')
        liver_amount=self.get_argument('liver_amount')
        bed_info=self.get_argument('bed_info')
        cash_money=self.get_argument('cash_money')
        least_day=self.get_argument('least_day')
        most_day=self.get_argument('most_day')
        ancillary_facility=self.get_argument('ancillary_facility')

        #获取该用户id
        mobile=self.get_secure_cookie('mobile').decode('utf8')
        cursor=self.db.cursor()
        sql="select id from user where mobile='"+mobile+"'"
        self.db.ping(reconnect=True)
        cursor.execute(sql)
        user_id=cursor.fetchone()[0]

        #存储数据
        sql2="insert into it_public_house(house_image_url, house_name, price, location, detail_addr, house_amount, house_area, house_account, liver_amount, bed_info, cash_money, least_day, most_day, ancillary_facility, user_id) " \
             "VALUES ('"+house_image_url+"','"+house_name+"','"+price+"','"+location+"','"+detail_addr+"','"+house_amount+"','"+house_area+"','"+house_account+"','"+liver_amount+"','"+bed_info+"','"+cash_money+"','"+least_day+"','"+most_day+"','"+ancillary_facility+"','"+str(user_id)+"')"
        self.db.ping(reconnect=True)
        cursor.execute(sql2)
        self.db.commit()
        self.db.close()

        self.write({'code':200})



class HouseImageHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        file=self.request.files

        file_img=file.get('file')

        #判断是否有图片
        if file_img:
            #生成随机字符串
            filename=str(time.strftime('%Y%m%d%H%M%S'))+'.jpg'
            img=file_img[0]['body']
            print(img)
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


            self.write({'code':200,'file_path':file_path})
        else:
            self.write({'code':300})


class ClientOrdersHandler(BaseHandler):
    def get(self):



        #在客户订单表中拿数据
        mobile=self.get_secure_cookie('mobile').decode('utf8')
        cursor=self.db.cursor()
        sql="select client_id , ico.id,house_image_url,house_name,create_time,live_time,left_time,monney,order_status,evaluate from user inner join it_client_orders ico on user.id = ico.user_id where mobile='"+mobile+"'"
        self.db.ping(reconnect=True)
        cursor.execute(sql)
        ret=cursor.fetchall()


        lis=[]

        for x in ret:
            li = []
            # 获取客户电话号码
            sql2 = "select mobile from user where id='" + str(x[0]) + "'"
            self.db.ping(reconnect=True)
            cursor.execute(sql2)
            client_mobile = cursor.fetchone()[0]
            print(client_mobile)

            li.append(client_mobile)
            li.append(x[1])
            li.append(x[2])
            li.append(x[3])
            li.append(x[4])
            li.append(x[5])
            li.append(x[6])
            li.append(x[7])
            li.append(x[8])
            li.append(x[9])
            lis.append(li)
        self.db.close()

        print(ret)
        self.render('clientorders.html',ret=lis)

    def post(self):
        pass


#退出登录
class ShutDownHandler(BaseHandler):
    def get(self):
        self.clear_cookie('mobile')
        self.clear_cookie('isregister')
        self.redirect('http://192.168.202.143:8888/')

    def post(self):
        pass




