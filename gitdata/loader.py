"""
This module allows you to initialize database.
"""
import sys
import types

__author__ = 'Trofimov Igor'


class GitHubFinder:
    """
    This class provides searching of module.
    """

    @classmethod
    def find_module(cls, fullname, path=None):
        name = fullname.split('.')
        if 'gitdata' in name and 'github' in name:
            return GitHubLoader


class GitHubLoader:
    """
    This class provides the dynamic loading of module.
    """

    @classmethod
    def load_module(cls, fullname):
        name = fullname.split('.')

        if len(name) < 4:
            module = types.ModuleType(fullname)
            module.__file__ = 'github_db:' + fullname
            module.__path__ = [fullname]
            module.__loader__ = GitHubLoader
            sys.modules.setdefault(fullname, module)
            return module
        else:
            from . import worker
            w = worker.Worker(name[2], name[3])
            sys.modules.setdefault(fullname, w)
            return w


sys.meta_path.append(GitHubFinder)
