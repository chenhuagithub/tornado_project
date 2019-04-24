# 数据源，数据库
container = {}

# 自定义 Session 方法
class Session():

    def __init__(self, handler):

        self.handler = handler      # 定义 handler, 这样可以再 Session 方法中获取 cookie 信息。
        self.randomStr = None       # 定义 self.randomStr ，防止有重复的 cookie 写入到客户端。

    def __GenarateRandomStr(self):  # 作用是生成随机的字符串，最后会以 value 发送给客户端当做登录识别码
        import hashlib
        import time
        obj = hashlib.md5()
        obj.update(bytes(str(time.time()), encoding="utf-8")) # 以当前时间戳设置 md5 值，得出随机字符串
        randomStr = obj.hexdigest()
        return randomStr

    def __setitem__(self, key, value):

        if not self.randomStr: # 如果是第一次执行则会进行下面的操作，如果不是第一次执行，则 self.randomeStr 则会拥有数据，以防止重复调用 __GenarateRandomStr 函数进行写入 cookie 信息的逻辑

            randomStr = self.handler.get_cookie("xarfToken") # 获取页面中的 cookie 是否拥有 xarfToken 值

            if not randomStr:                           # 如果没有 xarfToken 的值，则视为第一次访问
                randomStr = self.__GenarateRandomStr()  # 生成随机字符串
                container[randomStr] = {}               # 把随机字符串以 JSON 格式，放在数据库中
            else:
                if randomStr in container.keys():       # 如果有 xarfToken 的值，则数据是否在数据库中
                    pass
                else:                                   # 如果不在数据库中则视为伪造数据，并执行新建 xarfToken 值操作
                    randomStr = self.__GenarateRandomStr()
                    container[randomStr] = {}

            self.randomStr = randomStr                  # 把最终生成的 randomStr 数据赋给 self.randomStr，防止复用 __GenarateRandomStr 函数

        container[self.randomStr][key] = value          # 执行赋值操作

        return self.handler.set_cookie("xarfToken", self.randomStr) # 提交赋值数据

    def __getitem__(self, item):

        randomStr = self.handler.get_cookie("xarfToken") # 获取页面中的 cookie 是否拥有 xarfToken 值

        if not randomStr:                                # 如果没有 xarfToken 值，则视为没有数据
            return None

        userInfoDict = container.get(randomStr, None)
        if not userInfoDict:                             # 如果有 xarfToken 值，则查看在数据库中是否有值，如果没有则视为伪造数据返回空值
            return None

        return userInfoDict.get(item, None)              # 如果数据库中有值，则把数据库中的值获取并返回

