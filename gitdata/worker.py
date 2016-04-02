"""
This module allows you to use github.com as database.
"""

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

    def info(self):
        return {'login': self.username, 'repository': self.repository}
