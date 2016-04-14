import json
import os
import sys
import types
from subprocess import Popen

__all__ = ['git_import']


class GitHubModule:
    def __init__(self, user, repo):
        self._user = user
        self._repo = repo
        self._clone()

    def _clone(self):
        self.repo_root = os.path.join(os.getcwd(), "github_modules")
        if not os.path.exists(self.repo_root):
            os.mkdir(self.repo_root)
        self.repo_dir_name = self._user + "/" + self._repo
        self.repo_dir = os.path.join(self.repo_root, self.repo_dir_name)
        if os.path.exists(self.repo_dir):
            code = self._pull()
        else:
            code = Popen(
                "git clone https://github.com/%s/%s.git %s -q"
                % (self._user, self._repo, self.repo_dir)).wait()
        if code != 0:
            raise ImportError('ImportWithGitHub: bad module name %s.%s' % (self._user, self._repo))

    def _pull(self):
        if Popen("git -C %s fetch --all -q" % self.repo_dir).wait() == 0:
            if Popen("git -C %s reset --hard origin/master -q" % self.repo_dir).wait() == 0:
                return Popen("git -C %s pull -q" % self.repo_dir).wait()
        return 404

    def load(self, names):
        if self._pull() == 0:
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