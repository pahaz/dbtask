#!/usr/bin/python3

import sys
import types
from . import gitloader

__author__ = "KVS"

class GITImporter(object):

    def find_module(self, fullname, path=None):
        if fullname.startswith('gitdata.github'):
            return self

    def load_module(self, fullname):
        if not fullname.startswith('gitdata.github'):
            raise ImportError("GITImporter: It's not my business")
        path = fullname.split('.')[2:]
        
        if len(path) < 2:
            mod = types.ModuleType(fullname)
            mod.__fyle__ = "https://github.com/"+'/'.join(path)
            mod.__path__ = [mod.__fyle__]
            mod.__loader__ = self
            sys.modules.setdefault(fullname, mod)
            return mod

        path = "https://github.com/"+'/'.join(path)+".git"
        mod = gitloader.GITLoader(path)
        sys.modules.setdefault(fullname, mod)
        return mod

sys.meta_path.append(GITImporter())