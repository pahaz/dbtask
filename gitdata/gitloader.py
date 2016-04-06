#!/usr/bin/python3

import os
import json

class GITLoader(object):

    def __init__(self, gitpath):
        self.__gitpath = gitpath
        self.__mainpath = os.getcwd()
        d = self.__gitpath.split("/")[-1][:-4]
        self.__modulepath = "{}/{}/{}".format(self.__mainpath, ".gitdata", d)

        if ".gitdata" not in os.listdir():
            os.mkdir(".gitdata")
        os.chdir(".gitdata")

        if os.system("git --version >{}".format(os.devnull)):
            raise OSError("GITLoader: No git in PATH")

        if d in os.listdir():
            os.chdir(d)
            if os.system("git pull -q -r"):
                t = "GITLoader: git can't pull repo: {}".format(gitpath)
                raise ConnectionError(t)
        else:
            if os.system("git clone {} -q".format(self.__gitpath)):
                t = "GITLoader: git can't clone repo: {}".format(gitpath)
                raise ConnectionError(t)

        os.chdir(self.__mainpath)

    def load(self, listpath):
        for i in listpath:
            OK = False
            for tp in GITLoader.__types:
                fullpath = "{}/{}.{}".format(self.__modulepath, i, tp)
                if self.__check_exists(fullpath):
                    GITLoader.__types[tp](self, fullpath, i)
                    OK = True
            if not OK:
                print("Can't load {}", i)


    def __json_load(self, path, name):
        with open(path) as fin:
            setattr(self, name, json.load(fin))

    def __check_exists(self, fullpath):
        try:
            os.stat(fullpath)
        except:
            return False
        return True

    __types = {
        'json': __json_load
    }



