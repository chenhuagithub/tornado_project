# from fdfs_client.client import Fdfs_client
# import os
# client=Fdfs_client(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'fastdfs/client.conf'))
# ret=client.upload_by_filename('/home/chenhua/PycharmProjects/tornado_project/statics/img/01.jpg')
# print(ret)
#
# import os
# print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# import time
# print(time.time())
# print(time.strptime('1555932201.2329571','%a %b %d %H:%M:%S %Y'))

a={'price': 345, 'location': '霞山区', 'id': 1, 'public_time': '2019-04-23 09:46:05'}
b={'price': 123, 'location': '麻章区', 'id': 2, 'public_time': '2019-04-23 09:46:05'}
c={'price': 23, 'location': '赤坎区', 'id': 3, 'public_time': '2019-04-23 09:46:05'}
li=[]
li.append(a)
li.append(b)
li.append(c)
print(li)