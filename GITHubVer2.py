import random
import string

import requests


class GitHubApi:
    def __init__(self):
        self.SEARCH_STRINGS = ['def', 'continue', 'for']
        self.user_names = []
        self.file_urls = []
        self.processed_user_names = set([])

    def get_usernames(self):
       
        #It is to get items and then usernames
        
        response = requests.get(
            'https://api.github.com/search/repositories?q=language:python')
        if not response.ok:
            return False
        items = response.json()['items']
        for item in items:
            login = item['owner']['login']
            if login not in self.processed_user_names:
                self.user_names.append(login)
        return True

    def search_for_data(self):
         
        for search_string in self.SEARCH_STRINGS:
            for user_name in self.user_names:
                response = requests.get(
                    'https://api.github.com/search/code?q=%s+language:python+user:%s' % (search_string, user_name))
                if not response.ok:
                    break
                items = response.json()
                if 'items' in items:
                    for item in items['items']:
                        self.file_urls.append(item['url'])

    def get_random_name(self):
        return ''.join((random.choice(string.ascii_lowercase) for x in range(5)))

    def get_files(self):
         
        for url in self.file_urls:
            response = requests.get(url)
            if not response.ok:  # error happened
                break
            item = response.json()
            if 'download_url' not in item:
                continue
            download_url = item['download_url']
            response = requests.get(download_url)
            file_content = response.text
            with open("files/%s" % self.get_random_name(), "w", encoding='utf-8') as text_file:
                text_file.write(file_content)

    def save_processed_user_names(self):
        with open("processed_user_names.txt", "a+", encoding='utf-8') as text_file:
            for user_name in self.user_names:
                text_file.write('%s\n' % user_name)
            text_file.write('\n')

    def load_processed_user_names(self):
        self.processed_user_names = []
        with open("processed_user_names.txt", "r", encoding='utf-8') as text_file:
            content = text_file.read()
            for line in content.split('\n'):
                self.processed_user_names.append(line)

    def run(self):
         
        self.load_processed_user_names()
        is_successful = self.get_usernames()
        if is_successful:
            self.search_for_data()
            self.get_files()
            self.save_processed_user_names()


github_api = GitHubApi()
github_api.run()
