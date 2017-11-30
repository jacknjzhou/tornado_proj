#!-*-coding:utf8-*-
"""
@desc:统一的获取配置文件conf/conf.ini中的相关配置信息
"""
from config import Conf

conf_obj = Conf()

def get(section,key,default):
    """"""
    return conf_obj.get(section,key,default)

def get_init(section,key,deault):
    """"""
    return conf_obj.get_int(section,key,default)

def get_boolean(section,key,default):

    return conf_obj.get_boolean(section,key,default)