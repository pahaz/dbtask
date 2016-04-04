import getpass
import types
import sys
import os
import json

__author__ = 'atnes'
_cache = {}


class JsonKeeper:
    def __init__(self, json_obj):
        self.json_obj = json_obj

    def append(self, json_obj):
        print(self.json_obj, "appending!", json_obj)
        self.json_obj.append(json_obj)

    def get_json_obj(self):
        return self.json_obj

    def __str__(self):
        return str(self.json_obj)


class RepoBaseClass:
    def __init__(self):
        self.repo = None
        self.repo_dir = None
        self.jsons = {}
        self.keepers = {}

    def get_repo(self):
        return self.repo

    def load(self, modules):
        for module in modules:
            with open(os.path.join(self.repo_dir, module+".json")) as f:
                data = json.load(f)
                self.jsons[module] = data

    def __getattr__(self, item):
        if item not in self.jsons:
            return None
        if item not in self.keepers:
            self.keepers[item] = JsonKeeper(self.jsons[item])
        return self.keepers[item]

    def save(self, modules):
        for module in modules:
            module_dir = os.path.join(self.repo_dir, module+".json")
            with open(module_dir, "w") as f:
                json_obj = self.__getattr__(module).get_json_obj()
                f.write(json.dumps(json_obj))
                os.system("git -C '%s' add '%s'" % (self.repo_dir, module_dir))
        print("User:")
        user = input()

        passw = getpass.getpass(prompt="Password for %s:\n" % user)
        #passw = ""
        os.system("git -C '%s' remote set-url origin https://%s:%s@github.com/%s/%s.git --push" %
                  (self.repo_dir, user, passw, self.repo[0], self.repo[1]))
        os.system("git -C '%s' commit -am 'modules `%s` update' -q" % (self.repo_dir, str(modules)))
        os.system("git -C '%s' push origin master -q" % self.repo_dir)





def code_init(class_name):
    code = 'class {}(RepoBaseClass):' \
           '\n\tdef __init__(self, repo, repo_dir):' \
           '\n\t\tRepoBaseClass.__init__(self)' \
           '\n\t\tself.repo=repo' \
           '\n\t\tself.repo_dir = repo_dir'
    code = code.format(class_name, class_name)
    return code


class IGithubImportHook(object):
    def find_module(self, fullname, path=None):
        if fullname.startswith('gitdata'):
            return self

    def load_module(self, fullname):
        doted_fullname = fullname.split(".")
        if doted_fullname[0] != 'gitdata':
            raise ImportError('IGithubImportHook: bad module name ' + fullname)

        if len(doted_fullname) < 4:
            module = types.ModuleType(fullname)
            module.__file__ = "fake:" + fullname
            module.__path__ = [fullname]
            module.__loader__ = self
            sys.modules.setdefault(fullname, module)
            return module

        user = doted_fullname[2]
        module_name = doted_fullname[3]
        repo_root = os.path.join(os.getcwd(), "python_igithub_modules")
        repo_dir = os.path.join(repo_root, user+"."+module_name)

        if os.path.exists(repo_root):
            os.system("git -C  '%s' fetch --all -q" % repo_dir)

            os.system("git -C  '%s' reset --hard origin/master -q" % repo_dir)
        else:
            os.mkdir(repo_root)
            os.system(
               "git  clone https://github.com/%s/%s.git %s -q "
               % (user, module_name, repo_dir),
           )
        sys.path.insert(0, repo_dir)

        try:
            exec(code_init(module_name))
            module = eval(module_name+"({}, '{}')".format(doted_fullname[2:], repo_dir))
            _cache[fullname] = module
            sys.modules[fullname] = module
            return module
        except ImportError:
            sys.path.pop(0)
            raise




def main():
    sys.meta_path.insert(0, IGithubImportHook())
    import gitdata.github.atnesness.dbtask as db
    db.load(["users"])
    print(db.users)
    db.users.append({"name": "test2"})
    db.save(["users"])
    print(db.users)


if __name__ == "__main__":
    main()