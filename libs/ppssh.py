#!-*-coding:utf8-*-
"""
@author:
@date:
@desc:
"""
import time
import paramiko

SSH_DEFAULT_CONN_TIMEOUT = 5 #建立连接时的默认超时时间
SSH_DEFUALT_PORT = 36000 #建立连接时的默认端口
SSH_EXEC_CMD_TIMEOUT = 180 #执行命令时的默认超时时间

SSH_RETRY_NUM = 5  #尝试连接的最大次数

class PPSSHClient(object):

    def __init__(self):
        self._ssh = None
        

    def __del__(self):
        """"""
        print "call __del__ function"
        if self._ssh is not None:
            self._ssh.close()
    def close(self):
        """function:主动关闭"""
        if self._ssh is not None:
            self._ssh.close()
            self._ssh = None

    def _init(self):
        """function:初始化操作obj"""
        if self._ssh is not None:
            return
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.load_system_host_keys()

    def _conn(self,hostname,port,username=None,password=None,timeout=SSH_DEFAULT_CONN_TIMEOUT):
        """function:"""
        ret = True
        try:
            self._ssh.connect(hostname=hostname,port=port,username=username,password=password)

        except Exception,e:
            print str(e)
            ret = False

        return ret


    def connect(self,hostname,port,username,password,timeout=SSH_DEFAULT_CONN_TIMEOUT):
        """function:利用输入的参数进行尝试连接,可以用于验证端口/密码的有效性,也可以作为后续进行脚本执行和文件上传的连接入口"""
        self._init()

        ret = False
        i = 0
        while  True:
            ret = self._conn(hostname,port,username,password,timeout)
            if ret:
                break
            if i < SSH_RETRY_NUM:
                i = i + 1
            else:
                print "Retry Connect Too Many Times.Give Up!!!"
                break 
            print "Connect Fail,try later,sleep(0.5)..."
            time.sleep(0.2)
        return ret

class PPUploadFile(PPSSHClient):
    """function:执行文件上传操作"""
    def __init__(self):
        super(PPUploadFile,self).__init__()
        self._ftp_obj = None
        self._conn_result = False

    def __del__(self):
        if self._ftp_obj is not None:
            self._ftp_obj.close()
        if self._ssh is not None:
            self._ssh.close()

    def close(self):
        if self._ftp_obj is not None:
            self._ftp_obj.close()
        if self._ssh is not None:
            self._ssh.close()

    def _init(self):
        pass

    def _conn(self,hostname,port,username,password):
        """"""
        try:
            if self._ssh is not None:
                return True
            self._ssh = paramiko.Transport((hostname,port))
            self._ssh.connect(username=username,password=password)
            result = True
        except Exception,e:
            print str(e)
            result = False
        return result

    def run(self,**kwargs):
        """"""
        try:
            code = 1
            msg = ""
            result = False
            result = self.connect(hostname=kwargs.get("host"),port=kwargs.get("port"),
                                    username=kwargs.get("username"),password=kwargs.get("password"))
            if result:
                result = self.upload_file(kwargs.get("src_file"),kwargs.get("dest_file"))
                if result:
                    code = 0
                    msg = "OK"
                else:
                    msg ="Fail"

            else:
                msg = "[PPExecCmd]connect host fail."

        except Exception,e:
            print str(e)
            msg = str(e)
            code = 1
            result = False
        return code,msg

    def connect(self,hostname,port,username,password):
        result = self._conn(hostname,port,username,password)
        if result:
            self._ftp_obj = paramiko.SFTPClient.from_transport(self._ssh)
            self._conn_result = True
        return result

    def upload_file(self,src_path_file,dest_path_file):
        """
        function:执行文件上传操作(src_path_file需指定具体的文件,dest_path_file可以是目录)
        其中的src_path_file 指的是运行服务的本地目录,此处需要写一页面来执行进行文件上传操作,
        记录文件的路径名称,以方便进行管理文件
        """
        try:
            result = False
            if self._conn_result:
                self._ftp_obj.put(src_path_file,dest_path_file)
                result = True
            else:
                print "[upload_file]create connection fail."
        except Exception,e:
            print str(e)
            result =False
        return result


class PPExecCmd(PPSSHClient):
    """function:远程执行命令"""
    def __init__(self):
        super(PPExecCmd,self).__init__()

    def run(self,**kwargs):
        try:
            code = 1
            msg = ""
            result = False
            result = self.connect(hostname=kwargs.get("host"),port=kwargs.get("port"),
                                    username=kwargs.get("username"),password=kwargs.get("password"))
            if result:
                result,outinfo,outerr = self.exec_script_cmd(kwargs.get("cmd"))
                if result:
                    code = 0
                msg = str(outinfo)+"\n"+str(outerr)

            else:
                msg = "[PPExecCmd]connect host fail."
        except Exception,e:
            print str(e)
            msg = str(e)
            code = 1
            result = False
        return code,msg

    def exec_script_cmd(self,cmd_str,timeout=SSH_EXEC_CMD_TIMEOUT,buf_size=-1):
        """function:执行命令,并进行捕获执行的输出信息"""
        try:
            result = True

            std_out = ""
            std_err = ""

            trans_obj = self._ssh.get_transport()
            chains_obj = trans_obj.open_session()
            chains_obj.settimeout(timeout)
            #
            chains_obj.exec_command(cmd_str)

            stdin = chains_obj.makefile('wb',buf_size)
            stdout = chains_obj.makefile('rb',buf_size)
            stderr = chains_obj.makefile('rb',buf_size)

            std_out = stdout.read()
            std_err = stderr.read()
        except Exception,e:
            result = False
            print str(e)
            std_err = str(e)
        return result,std_out,std_err

if __name__ == '__main__':
    # pp_cmd = PPExecCmd()
    # result = pp_cmd.connect('127.0.0.1',22,'jackson','jackson')
    # print result
    # result,out_info,err_info = pp_cmd.exec_script_cmd("cd /tmp/;ls -al")
    # print result
    # print "Normal output:"
    # print out_info
    # print "Error output:"
    # print err_info
    info = {"host":"127.0.0.1","port":22,"username":"jackson","password":"jackson","src_file":"/Users/jackson/proj/cloud_proj/tornado_proj/test/cmd.json.txt","dest_file":"/tmp/cmd.json.txt"}

    pp_upload = PPUploadFile()
    result,msg = pp_upload.run(**info)
    print result,msg

