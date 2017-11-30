#!-*-coding:utf8-*-
try:
    import simplejson as json
except:
    import json

import traceback

ffrom voluptuous import Required, All, Length, Range, Schema

VERSION_LIST =["v1","v2"]

"""
@desc:此处为统一的接口请求参数校验,暂时未完成,后续完善
request base struct, example as follows:
example-1:
{
    "header":{
        "operator":"",
        "version":""
    },
    "body":{
        "data":{
            
        }
    }
}

"""

def check_schema_all(req_data = {}):
    """"""
    try:
        schema = Schema({"header":And({},),"body":And({},)},ignore_extra_keys=True)
        return schema.validate(req_data)

    except Exception,e:
        print traceback.format_exc()
        print str(e)
        return ""


def schema_check(req_data =""):

    schema_define = Schema(And(Use(json.loads),{
        'header':{
                "operator":And(str,),
                "version":And(Use(str,len),lambda n: n in VERSION_LIST)
                },
        'body':{
                    "data":{And({},)}
                }
            }
            ))
    try:
        result = True
        msg = ""

        schema = schema_define.validate(req_data)
    except Exception,e:
        import traceback
        print traceback.format_exc()
        schema = {}
        msg = str(e)
        result = False


    return result,msg,schema

if __name__ == '__main__':
    info = {
    "header":{
        "operator":"",
        "version":"v1"
    },
    "body":{
    }
}

    schema = check_schema_all(info)
    print schema


