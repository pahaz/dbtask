"""
This module allows you to use github.com as database.
"""
import json
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

    def _check_local_repository(self) -> bool:
        """
        Check for a local repository.

        :rtype: bool
        :return: True/False/None
        """
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

    def clone_repository(self) -> bool:
        """
        Clone remote repository.

        :rtype: bool
        :return: True/False/None
        """
        if self._check_local_repository():
            return True
        elif self._check_local_repository() is None:
            return None
        os.system('git clone -q git@github.com:{0}.git {0}'.format(self.link))
        if self._check_local_repository():
            return True
        return False

    def info(self) -> dict:
        """
        Return a dict with login and repository which module got.

        :rtype: dict
        :return: login and repository name
        """
        return {'login': self.username,
                'repository': self.repository}

    def load(self, names: list) -> bool:
        """
        Update files from github.com adn load database files to attributes.

        :type names: list with str
        :param names: contains the names of the database files
        :rtype: bool
        :return: True
        """
        os.system('cd {0} && git pull -q'.format(self.link))
        for name in names:
            if os.path.exists('{0}/{1}.json'.format(self.link, name)):
                with open('{0}/{1}.json'.format(self.link, name), 'r') as db_file:
                    self.__setattr__(name, json.loads(db_file.read()))
            else:
                raise KeyError('GitHubWorker: file {0} not found'.format(name))
        return True

    def save(self, names: list) -> bool:
        """
        Save data from attributes to files and push them to github.com

        :type names: list with str
        :param names: contains the names of the database files
        :rtype: bool
        :return: True
        """
        os.system('cd {0} && git pull -q'.format(self.link))
        for name in names:
            with open('{0}/{1}.json'.format(self.link, name), 'w') as db_file:
                db_file.write(json.dumps(self.__getattribute__(name)))
                os.system('git add {0}/{1}.json'.format(self.link, name))
        os.system('cd {0} && git commit -qam "Save {1}" && git push -q'.format(self.link, str(names)))
        return True
