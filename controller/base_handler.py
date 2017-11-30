#!-*-coding:utf8-*-
try:
    import simplejson as json
except:
    import json

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get(self):
         pass
    
    def post(self):
         pass

    def add_header(self,**kwargs):
        self.set_header("Content-Type","application/json")

    def return_info(self,data={}):
        """function:增加返回信息的统一格式"""
        try:
            self.add_header()
            self.write(json.dumps(data))
        except Exception,e:
            r_data ={"code":100,"msg":str(e)}
            self.write(json.dumps(r_data))