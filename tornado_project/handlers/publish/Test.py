from handlers.base.BaseHandler import BaseHandler
from PIL import Image
import os
import time

class TestHandler(BaseHandler):
    def get(self):
        self.render('login2.html')

    def post(self):
        file=self.request.files
        print(file)
        #用时间生成随机字符串作为文件名，以保证文件名的唯一
        filename=time.strftime('%Y%m%d%H%M%S')+'.jpg'
        file_img=file.get('file')
        print(file_img)
        if file_img:
            # 获取图片
            img=file_img[0]['body']
            #创建一个路径存储图片
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'bufferimage/'+filename),'wb') as f:
                f.write(img)

        self.write({'info':0})

# #
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
# username='陈hua'
# mobile='13267869217'
# sql="select username from user where mobile='13267869217'"
#
#
#
# cursor.execute(sql)
# ret=cursor.fetchone()
# print(ret)
# # connection.commit()
# connection.close()




# connection.commit()
# connection.close()