from handlers.base.BaseHandler import BaseHandler

class HouseResourceHandler(BaseHandler):
    def get(self):
        self.render('houseresource.html')

    def post(self):
        pass

