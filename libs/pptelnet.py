#!-*-coding:utf8-*-
import telnetlib
import traceback

DEFAULT_TIMEOUT = 2

class CheckPort(object):
    """function:基本的检查指定设备端口的连通性"""
    def __init__(self):
        pass

    def check_telnet(self,ip,port,timeout=DEFAULT_TIMEOUT):
        """fucntion:检查端口的连通性"""
        try:
            if not isinstance(port,int):
                port = int(port)
            conn = None
            conn = telnetlib.Telnet(ip,port,timeout)
            result = True
        except Exception,e:
            print str(e)
            #print traceback.format_exc()
            result =False
        finally:
            if conn is not None:
                conn.close()
        return result

if __name__ == '__main__':
    ck_obj = CheckPort()
    result = ck_obj.check_telnet('127.0.0.1',22,2)
    print result
    result = ck_obj.check_telnet('127.0.0.1',20,2)
    print result