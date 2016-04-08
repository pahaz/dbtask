import json
import os
import sys
import types

__all__ = ['git_import']


class GitHubModule:
    def __init__(self, user, repo):
        self.user = user
        self.repo = repo
        self._clone()

    def _clone(self):
        self.repo_root = os.path.join(os.getcwd(), "github_modules")
        self.repo_dir_name = self.user + "/" + self.repo
        self.repo_dir = os.path.join(self.repo_root, self.repo_dir_name)
        if os.path.exists(self.repo_dir):
            os.system("cd %s && git pull -q" % self.repo_dir)

        else:
            os.mkdir(self.repo_root)
            os.system(
                "git clone https://github.com/%s/%s.git %s -q"
                % (self.user, self.repo, self.repo_dir),
            )

    def load(self, names):
        os.system("cd %s && git pull -q" % self.repo_dir)
        for name in names:
            file_name = "%s/%s.json" % (self.repo_dir, name)
            if os.path.exists(file_name):
                with open(file_name, 'r') as file:
                    self.__setattr__(name, json.loads(file.read()))


class ImportWithGitHub(object):
    def find_module(self, fullname, path=None):
        if fullname.startswith('gitdata'):
            return self

    def load_module(self, fullname):
        module_name = fullname.split('.')

        if len(module_name) < 4:
            module = types.ModuleType(fullname)
            module.__file__ = "fakegithub:" + fullname
            module.__path__ = [fullname]
            module.__loader__ = self
            sys.modules.setdefault(fullname, module)
            return module

        if module_name[:2] != ['gitdata', 'github']:
            raise ImportError('ImportWithGitHub: bad module name ' + fullname)
        module = GitHubModule(module_name[2], module_name[3])
        sys.modules.setdefault(fullname, module)
        return module


def git_import():
    sys.meta_path.append(ImportWithGitHub())