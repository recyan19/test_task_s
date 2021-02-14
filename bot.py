import json
import random
import string
import requests


class AutoBot:
    def __init__(self, path):
        self.settings = self.read_settings(path)
        self.bot_settings = self.settings['bot_settings']
        self.urls = self.get_urls()
        self.users = []
        self.posts = []

    @staticmethod
    def read_settings(path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def get_urls(self):
        urls_dict = self.settings['urls']
        for k, v in urls_dict.items():
            if k != 'base_url':
                urls_dict[k] = urls_dict['base_url'] + v
        return urls_dict

    @staticmethod
    def get(url, token=None):
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.get(url, headers=headers)
        return r.json()

    @staticmethod
    def post(url, data=None, token=None):
        headers = {'Authorization': f'Bearer {token}'} if token else None
        r = requests.post(url, data=data, headers=headers)
        return r.json()

    @staticmethod
    def gen_rand_string(length=8):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
        return result_str

    def create_users(self):
        signup_url = self.urls['signup_url']
        token_url = self.urls['get_token_url']
        for i in range(self.bot_settings['number_of_users']):
            data = {
                "username": self.gen_rand_string(),
                "password": self.gen_rand_string()
            }
            self.post(signup_url, data=data)
            data['token'] = self.post(token_url, data=data)['access']
            self.users.append(data)

    def create_posts(self):
        for u in self.users:
            num_posts = random.randint(1, self.bot_settings['max_posts_per_user'])
            for i in range(num_posts):
                data = {
                    'title': self.gen_rand_string(32),
                    'text': self.gen_rand_string(128)
                }
                url = self.urls['post_create_url']
                post_data = self.post(url, data=data, token=u['token'])
                self.posts.append(post_data)

    def create_likes(self):
        max_likes_num = self.bot_settings['max_likes_per_user']
        for u in self.users:
            posts = self.posts[:]
            random.shuffle(posts)
            num_likes = random.randint(1, max_likes_num)

            for i in range(num_likes):
                post = posts.pop()
                url = self.urls['post_like_url'].format(post_id=post['id'])
                self.post(url, {}, u['token'])

    def run(self):
        self.create_users()
        self.create_posts()
        self.create_likes()


if __name__ == '__main__':
    bot = AutoBot('bot_config.json')
    bot.run()
