#!-*-coding:utf8-*-
try:
    import simplejson as json
except:
    import json

from controller.base_handler import BaseHandler


class APIHandler(BaseHandler):
    """function:演示接口"""
    def get(self):
        """function:get demo"""
        args = self.get_arguments("a")
        b = self.get_arguments('b')
        print b
        print args
        
        self.write(json.dumps({"code":0,"msg":"OK"}))

    def post(self):
        """function:post"""
        data = self.request.body
        print data
        self.write(json.dumps({"code":0,"msg":"OK"}))