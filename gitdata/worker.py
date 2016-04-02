"""
This module allows you to use github.com as database.
"""
import os


__author__ = 'Trofimov Igor'


class Worker:
    """
    This class provides all necessary functions for to work with github.
    """

    def __init__(self, username, repository):
        """
        Constructor for Worker
        """
        self.username = username
        self.repository = repository
        self.link = "{0}/{1}".format(username, repository)

    def _check_local_repository(self):
        if os.path.exists(self.link):
            if os.path.isdir(self.link):
                if os.path.exists(self.link + '/.git'):
                    if os.path.isdir(self.link + '/.git'):
                        # Repository already downloaded
                        return True
                # Dir already created. We can not use this dir
                return None
        # No dir. No repository. Ready to download
        return False

    def clone_repository(self):
        if self._check_local_repository() is None:
            return None
        os.system('git clone -q git@github.com:{0}.git {0}'.format(self.link))
        if self._check_local_repository():
            return True
        return False

    def info(self):
        return {'login': self.username,
                'repository': self.repository}

    def load(self, names):
        pass

    def save(self, names):
        pass
