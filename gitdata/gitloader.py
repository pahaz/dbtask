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
                os.chdir("..")
                os.system('rmdir /S /Q \"{}\"'.format(d))
                if os.system("git clone {} -q".format(self.__gitpath)):
                    t = "GITLoader: git can't clone repo: {}".format(gitpath)
                    raise ConnectionError(t)
        else:
            if os.system("git clone {} -q".format(self.__gitpath)):
                t = "GITLoader: git can't clone repo: {}".format(gitpath)
                raise ConnectionError(t)
            t = "git remote add origin ssh://git@github.com:{}/{}.git >{}"
            os.system(t.format(u, d, os.devnull))
        os.chdir(curpath)

    def load(self, listpath):
        for i in listpath:
            OK = False
            for tp in GITLoader.__types:
                fullpath = "{}/{}.{}".format(self.__modulepath, i, tp)
                if self.__check_exists(fullpath):
                    ld = GITLoader.__types[tp][0](self, fullpath)
                    OK = True
                    break
            if OK:
                p = i.split("/")
                k = self
                for j in p[:-1]:
                    if not hasattr(k, j):
                        t = LoaderProperty()
                        setattr(k, j, t)
                    k = getattr(k, j)
                setattr(k, p[-1], ld)
                self.__loaded[i] =  tp
            else:
                print("Can't load {}", i)

    def save(self, listpath):
        curpath = os.getcwd()

        os.chdir(self.__modulepath)
        
        t = ""
        for i in listpath:
            if i in self.__loaded:
                self.__save(i)
                t += "{}.{} ".format(i, self.__loaded[i])
        
        print("git add {}".format(t, os.devnull))

        if os.system("git add {}".format(t, os.devnull)):
            raise OSError("GITLoader: git can't add file from list")

        if os.system("git commit -m \"GITLoader: add {}\" -q".format(t)):
            raise OSError("GITLoader: Something goes wrong :-(")

        if os.system("ssh-agent ssh-add {} >{}".format("id_rsa", os.devnull)):
            raise OSError("GITLoader: Can't add id_rsa")

        if os.system("git push origin"):
            raise ConnectionError("GITLoader: Can't connect to repo")

        os.chdir(curpath)

    def __save(self, fl):
        p = fl.split("/")
        k = self
        for i in p:
            k = getattr(k, i)
        if fl in self.__loaded:
            fullpath = "{}/{}.{}".format(self.__modulepath, fl, self.__loaded[fl])
            self.__types[self.__loaded[fl]][1](self, fullpath, k)

    def __json_load(self, path):
        with open(path) as fin:
            return json.load(fin)

    def __json_save(self, path, obj):
        print(path)
        with open(path, 'w') as fout:
            json.dump(obj, fout)

    def __check_exists(self, fullpath):
        try:
            os.stat(fullpath)
        except:
            return False
        return True

    __types = {
        'json': (__json_load, __json_save)
    }
    __loaded = {}

class LoaderProperty():
    def __init__(self):
        pass


