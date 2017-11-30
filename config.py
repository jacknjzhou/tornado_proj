#!-*-coding:utf8-*-
import os
import ConfigParser

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

CONF_FILE = os.path.join(BASE_DIR,"conf/conf.ini")


class Conf(object):
    """"""
    def __init__(self,conf_file=CONF_FILE):
        self._conf_file = conf_file
        self._oconf = ConfigParser.ConfigParser()
        self._oconf.read(self._conf_file)

    def get(self,section,key,default=""):
        """"""
        try:
            return self._oconf.get(section,key)
        except Exception,e:
            print str(e)
            return default

    def get_int(self,section,key,default=0):
        """"""
        try:
            return self._oconf.getint(section,key)
        except Exception,e:
            print e
            return default

    def get_boolean(self,section,key,default=False):
        """"""
        try:
            return self._oconf.getboolean(section,key)
        except Exception,e:
            print e
            return default

    def get_single(self,section=""):
        """"""
        try:
            confs = {}
            if section:
                for sk,sv in self._oconf.items(section):
                    confs[sk] = sv
        except:
            pass
        return confs


if __name__ == '__main__':

    print BASE_DIR
    print CONF_FILE