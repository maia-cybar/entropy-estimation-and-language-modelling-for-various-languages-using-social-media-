import requests


class GitHubApi:
    def __init__(self):
        self.SEARCH_STRINGS = ['def', 'continue', 'for']
        self.user_names = []
        self.file_urls = []

    def get_usernames(self):
         
        response = requests.get(
            'https://api.github.com/search/repositories?q=language:python&sort=stars')
        items = response.json()['items']
        for item in items:
            self.user_names.append(item['owner']['login'])

    def search_for_data(self):
         
        for search_string in self.SEARCH_STRINGS:
            for user_name in self.user_names:
                response = requests.get(
                    'https://api.github.com/search/code?q=%s+language:python+user:%s' % (search_string, user_name))
                items = response.json()
                if 'items' in items:
                    for item in items['items']:
                        self.file_urls.append(item['url'])

    def get_files(self):
         
        num = 1
        for url in self.file_urls:
            response = requests.get(url)
            item = response.json()
            if 'download_url' not in item:
                continue
            download_url = item['download_url']
            response = requests.get(download_url)
            file_content = response.text
            with open("files/%d" % num, "w", encoding='utf-8') as text_file:
                text_file.write(file_content)
                num += 1

    def run(self):
         
        self.get_usernames()
        self.search_for_data()
        self.get_files()


github_api = GitHubApi()
github_api.run()