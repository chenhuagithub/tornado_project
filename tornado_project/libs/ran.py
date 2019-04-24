import random
import time

def ran():
    strs=''
    for x in range(4):
        strs+=str(random.randint(0,9))

    ti=time.strftime('%Y%m%d%H%M%S')
    print(type(ti))

    print(strs)


ran()
