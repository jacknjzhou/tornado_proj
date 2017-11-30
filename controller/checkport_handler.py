#!-*-coding:utf8-*-
try:
    import simplejson as json
except:
    import json
import traceback
# from schema import Schema,Optional
from controller.base_handler import BaseHandler
from libs.pptelnet import CheckPort
from libs.log import log
"""
@ desc:用于检查端口是否联通,
@ params:
{
    "header":{
        "operator":"",
        "version":""
    },
    "body":{
        "data":{
            "info_list":[{"ip":"127.0.0.1","port":22},{}]
        }
    }
}
响应格式: result ==>1 Ok / 0:Fail
{
    "msg": "OK", 
    "code": 0, 
    "details": [
                {"ip": "127.0.0.1", 
                "port": 22, 
                "result": 1}, 
                {"ip": "127.0.0.1", 
                "port": 20, 
                "result": 0}
            ]
}

"""

class CheckPortHandler(BaseHandler):
    """function:检查端口是否联通"""
    def get(self):
        print "[CheckPortHandler][get]..."
        ret_msg = {"code":1,"msg":"interface not support get method."}
        self.return_info(json.dumps(ret_msg))

    def post(self):
        """function:处理post请求"""
        try:
            log("[CheckPortHandler][post]start process...")
            f_data = {"code":0,"msg":"OK","details":[]}
            r_data = self.request.body
            r_data = json.loads(r_data)
            #step-1:check params
            r_result,r_msg = self.check_params(r_data)
            if not r_result:
                f_data["code"] = 1
                f_data["msg"] = r_msg
            else:
                chk_obj = CheckPort()
                #step-2:check port
                f_details = []
                r_info_device = r_data.get("body",{}).get("data",{}).get("info_list",[])

                for index, item in enumerate(r_info_device):
                    rc_result = chk_obj.check_telnet(item.get("ip"),item.get("port"))
                    rc_result = 1 if rc_result else 0
                    f_details.append({"ip":item.get("ip"),"port":item.get("port"),"result":rc_result})
                
                f_data["details"] = f_details

        except Exception,e:
            print traceback.format_exc()
            code = 100
            msg = str(e)
            f_data = {"code":code,"msg":msg}

        self.return_info(f_data)

    def check_params(self,req_data={}):
        """function:检查输入参数的有效性"""

        def _check_item(item={}):
            """function:check inner item"""
            if "ip" not in item or not item.get("ip",""):
                result = False
                msg = "Miss param[ip] or value is null."
                return result,msg

            if "port" not in item or not item.get("port",0):
                result = False
                msg = "Miss param[port] or value is null."
                return result,msg

            return True,"OK"


        r_header= req_data.get("header",{})
        r_body = req_data.get("body",{})

        result = True
        msg = "OK"

        r_data = r_body.get("data",{})
        if not r_data:
            result = False
            msg = "[CheckPortHandler][check_params]miss param[body.data],please check."
            return result,msg
        if not isinstance(r_data,dict):
            result = False
            msg = "[CheckPortHandler][check_params]param[body.data] value type must be dict,please check."
            return result,msg

        r_info_list = r_data.get("info_list",[])
        if not r_info_list:
            result = False
            msg = "[CheckPortHandler][check_params]miss param[info_list] or value is null,please check."
            return result,msg
        if not isinstance(r_info_list,list):
            result = False
            msg = "[CheckPortHandler][check_params]miss param[info_list] value type must be list,please check."
            return result,msg
        #check each item
        for index,item in enumerate(r_info_list):
            result,msg = _check_item(item)
            if not result:
                return result,msg

        return result,msg