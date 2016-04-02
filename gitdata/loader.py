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
    def find_module(cls, fullname: str, path: None = None) -> object:
        """
        Find our module

        :param path: Nothing interesting
        :type fullname: str
        :param fullname: Module's full name in search
        :rtype: GitHubLoader class
        :return: GitHubLoader class
        """
        name = fullname.split('.')
        if 'gitdata' in name and 'github' in name:
            return GitHubLoader


class GitHubLoader:
    """
    This class provides the dynamic loading of module.
    """

    @classmethod
    def load_module(cls, fullname: str) -> object:
        """
        Load our module

        :type fullname: str
        :param fullname: Module's full name in search
        :rtype: types.ModuleType or Worker class
        :return: module
        """
        name = fullname.split('.')

        if 'gitdata' not in name or 'github' not in name:
            raise ImportError('GitHubLoader: bad module name {0}'.format(fullname))
        if len(name) < 4:
            module = types.ModuleType(fullname)
            module.__file__ = 'github_db:' + fullname
            module.__path__ = [fullname]
            module.__loader__ = GitHubLoader
            sys.modules.setdefault(fullname, module)
            return module
        elif len(name) == 4:
            from . import worker
            module = worker.Worker(name[2], name[3])
            check = module.clone_repository()
            if check is None:
                raise ImportError('GitHubLoader: dir {0}/{1} already exists'.format(name[2], name[3]))
            elif check:
                sys.modules.setdefault(fullname, module)
                return module
            raise ImportError('GitHubLoader: bad user name {0} or repository name {1}'.format(name[2], name[3]))
        raise ImportError('GitHubLoader: bad module name {0}'.format(fullname))


sys.meta_path.append(GitHubFinder)
