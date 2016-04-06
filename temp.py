import types
import sys
import os

__author__ = 'pahaz'
_cache = {}


class IGithubImportHook(object):
    def find_module(self, fullname, path=None):
        if fullname.startswith('github'):
            return self

    def load_module(self, fullname):
        print('load_module', fullname)
        doted_fullname = fullname.split(".")
        if doted_fullname[0] != 'github':
            raise ImportError('IGithubImportHook: bad module name ' + fullname)

        if len(doted_fullname) < 3:
            module = types.ModuleType(fullname)
            module.__file__ = "fake:" + fullname
            module.__path__ = [fullname]
            module.__loader__ = self
            sys.modules.setdefault(fullname, module)
            return module

        user = doted_fullname[1]
        module_name = doted_fullname[2]
        repo_root = os.path.join(os.getcwd(), "python_igithub_modules")
        repo_dir = os.path.join(repo_root, module_name)

        if not os.path.exists(repo_root):
            os.mkdir(repo_root)

        if os.path.exists(repo_dir):
            os.system("git pull -q -C %s" % repo_dir)
        else:
            os.system(
                "git clone git://github.com/%s/%s.git %s -q"
                % (user, module_name, repo_dir),
            )

        sys.path.insert(0, repo_dir)

        try:
            module = __import__(module_name)
            print(module)
            print(dir(module))
            _cache[fullname] = module
            sys.modules[fullname] = module
            return module
        except ImportError:
            sys.path.pop(0)
            raise


sys.meta_path.insert(0, IGithubImportHook())