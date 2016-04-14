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

    def __init__(self, username: 'Строка имени пользователя GitHub',
                 repository: 'Строка названия репозитория GitHub') -> 'Объект класса Worker':
        """
        Constructor for Worker
        """
        self.username = username
        self.repository = repository
        self.__link = "{0}/{1}".format(username, repository)

    @property
    def link(self) -> 'Строка пути до удаленного репозитория':
        """
        Read path to remote repository.
        """
        return self.__link

    def _check_local_repository(self) -> 'Логический результат проверки возможности загрузки данных из репозитория':
        """
        Check for a local repository.
        """
        # FIXME os.path.isdir( os.path.join( self.link, '.git')) лучше
        if os.path.exists(self.link):
            if os.path.isdir(self.link):
                if os.path.exists(self.link + '/.git'):
                    if os.path.isdir(self.link + '/.git'):
                        # Repository already downloaded
                        return True
                # Dir already created. We can not use this dir
                # FIXME Плохой способ сигнализирования исключений
                return None
        # No dir. No repository. Ready to download
        return False

    def clone_repository(self) -> 'Логический результат попытки клонирования репозитория':
        """
        Clone remote repository.
        """
        if self._check_local_repository():
            return True
        elif self._check_local_repository() is None:
            return None
        # FIXME Заменить на subprocess
        os.system('git clone -q git@github.com:{0}.git {0}'.format(self.link))
        if self._check_local_repository():
            return True
        return False

    def info(self) -> 'Словарь из имени пользователя и названия репозитория':
        """
        Return a dict with login and repository which module got.

        :rtype: dict
        :return: login and repository name
        """
        return {'login': self.username,
                'repository': self.repository}

    def load(self, names: 'Список строк названий ' +
                          'файлов для загрузки') -> 'Логический результат попытки загрузки данных из файла':
        """
        Update files from github.com adn load database files to attributes.
        """
        # FIXME Заменить на subprocess
        os.system('cd {0} && git pull -q'.format(self.link))
        for name in names:
            if os.path.exists('{0}/{1}.json'.format(self.link, name)):
                with open('{0}/{1}.json'.format(self.link, name), 'r') as db_file:
                    self.__setattr__(name, json.loads(db_file.read()))
            else:
                raise KeyError('GitHubWorker: file {0} not found'.format(name))
        return True

    def save(self, names: 'Список строк названий ' +
                          'файлов для сохранения') -> 'Логический результат попытки сохранения данных в файл':
        """
        Save data from attributes to files and push them to github.com
        """
        # FIXME Заменить на subprocess
        # TODO Разрешение конфликтов
        os.system('cd {0} && git pull -q'.format(self.link))
        for name in names:
            with open('{0}/{1}.json'.format(self.link, name), 'w') as db_file:
                db_file.write(json.dumps(self.__getattribute__(name)))
                # TODO Тут тоже могут быть конфликты
                # FIXME Заменить на subprocess
                # TODO Указание файла ключа пользователем
                os.system('git add {0}/{1}.json'.format(self.link, name))
        # FIXME Заменить на subprocess
        os.system('cd {0} && git commit -qam "Save {1}" && git push -q'.format(self.link, str(names)))
        return True
