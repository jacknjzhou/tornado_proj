#-*-coding:utf8-*-
import os
import time
from config import Conf,BASE_DIR

# _CONF_FILE=os.getcwd()+'/conf.ini'

_LOG_DIR=None
_LOG_FILE=None
_LOG_LEVEL=None

_SVR_PORT=None
_PROJ_NAME=None
_SVR_TYPE=None

class Setting(object):
    
    @staticmethod
    def _get_current_path():
        '''function:get current path'''
        return os.getcwd()
    
    @staticmethod
    def _loadsetting():
        global _LOG_DIR,_LOG_LEVEL,_LOG_FILE,_SVR_PORT,_PROJ_NAME,_SVR_TYPE
        conf = Conf()

        _LOG_DIR=os.path.join(BASE_DIR,conf.get("LOG", "log.path", "logs"))
        # _SVR_PORT=conf.get_int("SVR","port",9999)
        _LOG_LEVEL=conf.get("LOG","log.level","info")
        _LOG_FILE=conf.get("LOG","log.file","log")
        _PROJ_NAME=conf.get("DEFAULT", "proj.name","proj")
        # _SVR_TYPE = conf.get("SVR","type","udp")
        return

# def get_type():
#     global _SVR_TYPE
#     if _SVR_TYPE is None:
#         Setting._loadsetting()
#     return _SVR_TYPE

def get_logdir():
    global _LOG_DIR
    if _LOG_DIR is None:
        Setting._loadsetting()
    return _LOG_DIR

def get_logfile():
    global _LOG_FILE
    if _LOG_FILE is None:
        Setting._loadsetting()
    return _LOG_FILE

def get_loglevel():
    global _LOG_LEVEL
    if _LOG_LEVEL is None:
        Setting._loadsetting()
    return _LOG_LEVEL

def get_svrport():
    global _SVR_PORT
    if _SVR_PORT is None:
        Setting._loadsetting()
    return _SVR_PORT

def get_projname():
    global _PROJ_NAME
    if _PROJ_NAME is None:
        Setting._loadsetting()
    return _PROJ_NAME