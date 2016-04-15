__author__ = 'Acedia'

import requests
import shutil

class GitHub:

    def __init__(self, log, pas):

        self.user = requests.get('https://api.github.com/user', auth=(log, pas))
        self.repo = requests.get('https://api.github.com/user/repos', auth=(log, pas))
        self.login = log
        self.password = pas



    def GetUser(self):
        begin = self.user.text.find('"login":') + len('"login":') + 1
        end = self.user.text.find('"id"') - 2
        return self.user.text[begin:end]

    def GetAvatar(self):
        begin = self.user.text.find('"avatar_url":') + len('"avatar_url":') + 1
        end = self.user.text.find('"gravatar_id"') - 2
        return self.user.text[begin:end]

    def GetRepo(self):
        list = []
        newRepo = self.repo.text
        while newRepo.find('"name":') >= 0:
            begin = newRepo.find('"name":') + 1 + len('"name":')
            end = newRepo.find("full_name") - 3
            list.append(newRepo[begin:end])
            newRepo = newRepo[end + len('full_name'):]
        return list

    def DownloadRepo(self, name):
        user = self.GetUser()
        user += '/' + name
        repoId = requests.get('https://api.github.com/repos/' + str(user), auth=(self.login, self.password))
        id = repoId.text[
            repoId.text.find('"id":') + len('"id":')
            :
            repoId.text.find(",",  repoId.text.find('"id":'))
        ]
        name = name + '.zip'
        repo = requests.get('https://api.github.com/repos/'+ str(user)+'/zipball/master', auth=(self.login, self.password))
        with open(name, 'wb') as code:
            code.write(repo.content)
        print("OK")


    def DownloadAvatar(self, url):
        response = requests.get(url, stream=True)
        with open('img.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

