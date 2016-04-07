#!/usr/bin/python3

import os
import json

class GITLoader(object):

    def __init__(self, gitpath):
        self.__gitpath = gitpath
        curpath = os.getcwd()
        t = self.__gitpath.split("/")
        u = t[-2]
        d = t[-1][:-4]
        self.__modulepath = "{}/{}/{}".format(curpath, ".gitdata", d)

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
            t = "git remote add origin ssh://git@github.com:{}/{}.git -q"
            os.system(t.format(u, d))
        os.chdir(curpath)

    def load(self, listpath):
        for i in listpath:
            OK = False
            for tp in GITLoader.__types:
                fullpath = "{}/{}.{}".format(self.__modulepath, i, tp)
                if self.__check_exists(fullpath):
                    ld = GITLoader.__types[tp](self, fullpath, i)
                    OK = True
            if OK:
                p = i.split("/")
                k = self
                for j in p[:-1]:
                    if not hasattr(k, j):
                        t = LoaderProperty()
                        setattr(k, j, t)
                    k = getattr(k, j)
                setattr(k, p[-1], ld)
            else:
                print("Can't load {}", i)

    def save(self, listpath):
        curpath = os.getcwd()

        os.chdir(self.__modulepath)
        
        t = ""
        for i in listpath:
            t += "{} ".format(i)
        
        if os.system("git add -q {}".format(t)):
            raise OSError("GITLoader: git can't add file from list")

        if os.system("git commit -m \"GITLoader: add {}\" -q".format(t)):
            raise OSError("GITLoader: Something goes wrong :-(")

        if os.system("ssh-agent ssh-add {} >{}".format("id_rsa", os.devnull)):
            raise OSError("GITLoader: Can't add id_rsa")

        if os.system("git push origin")

        os.chdir(curpath)


    def __json_load(self, path, name):
        with open(path) as fin:
            return json.load(fin)

    def __check_exists(self, fullpath):
        try:
            os.stat(fullpath)
        except:
            return False
        return True

    __types = {
        'json': __json_load
    }

class LoaderProperty():
    def __init__(self):
        pass


