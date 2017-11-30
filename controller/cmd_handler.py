#!-*-coding:utf8-*-
try:
    import simplejson as json
except:
    import json
import traceback
# from schema import Schema,Optional
from controller.base_handler import BaseHandler
from libs.ppssh import PPExecCmd

"""
@params host
@params port
@params username
@params password
@params cmd
"""

class CmdHandler(BaseHandler):

    def get(self):
        print "[CmdHandler][get]..."
        ret_msg = {"code":1,"msg":"interface not support get method."}
        self.return_info(json.dumps(ret_msg))

    def post(self):
        """"""
        try:
            f_data = {"code":0,"msg":"OK","details":[]}

            r_data = self.request.body
            # print r_data
            r_data = json.loads(r_data)

            #step-1:check params
            result,msg = self.check_params(r_data)
            if not result:
                f_data["code"] = 1
                f_data["msg"] = msg
            else:
                cmd_obj = PPExecCmd()
                req_data = r_data.get("body",{}).get("data",{})
                # print "*"*20
                # print json.dumps(req_data)
                code,msg = cmd_obj.run(**req_data)

                f_data["code"] = code
                f_data["msg"] = msg

        except Exception,e:
            print str(e)
            msg = str(e)
            f_data["code"] = 1
            f_data["msg"] = msg

        return self.return_info(f_data)


    def check_params(self,req_data = {}):
        """function:check params"""

        def _check_item(req_item={}):
            result = True
            msg = "OK"
            item_key = ["host","port","username","password","cmd"]
            for item in item_key:
                if item not in req_item:
                    result = False
                    msg = "[_check_item]param [%s]must be contained."%(item,)
                    return result,msg

            return result,msg

        r_header= req_data.get("header",{})
        r_body = req_data.get("body",{})

        result = True
        msg = "OK"

        r_data = r_body.get("data",{})
        if not r_data:
            result = False
            msg = "[CmdHandler][check_params]miss param[body.data],please check."
            return result,msg
        if not isinstance(r_data,dict):
            result = False
            msg = "[CmdHandler][check_params]param[body.data] value type must be dict,please check."
            return result,msg

        result,msg = _check_item(r_data)
        return result,msg