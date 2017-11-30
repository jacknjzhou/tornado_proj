#!-*-coding:utf8-*-
import tornado.ioloop
import tornado.web
import os
import tornado.autoreload
from tornado.options import options,define

from libs.log import log

from controller.api_handler import APIHandler
from controller.checkport_handler import CheckPortHandler
from controller.cmd_handler import CmdHandler
from controller.fileupload_handler import FileUploadHandler

define("port", default=8000,type=int,help="listen port")

settings = {
    "cookie_secret":"61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies":False,
    # "login_url":"/login",
    "static_path":os.path.join(os.path.dirname(__file__),"static"),
    "template_path":os.path.join(os.path.dirname(__file__),"templates"),
    "debug":True,
    "autoload":True
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

if __name__ == "__main__":
    """
    @func:服务运行入口,支持命令行输入端口
    """
    try:
        options.parse_command_line()
        log("start server...")
        print "start server...."
        application = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/api/checkport",CheckPortHandler),
            (r"/api/cmd",CmdHandler),
            (r"/api/file",FileUploadHandler),
            #(r"/api",APIHandler),
        ],**settings)
        log("listen on port %s..."%(str(options.port)))
        print "port listen on %s..."%(str(options.port))

        application.listen(options.port)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt,e:
        pass
    except Exception,e:
        print "Exception:",str(e)

