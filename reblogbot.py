# -*- coding: utf-8 -*-
from mastodon import Mastodon
import json
import configparser
from time import sleep

config = configparser.ConfigParser()
config.read('./config.ini')

API_BASE_URL = config.get("api", "API_BASE_URL")
USERNAME = config.get("auth", "USERNAME")
PASSWORD = config.get("auth", "PASSWORD")


class Bot:
    def __init__(self):
        Mastodon.create_app(
            client_name='reblogbot',
            api_base_url=API_BASE_URL,
            to_file='reblogbot_clientcred.txt'
        )

        self.pawoo = Mastodon(
            client_id='reblogbot_clientcred.txt',
            api_base_url=API_BASE_URL
        )

        self.pawoo.log_in(
            username=USERNAME,
            password=PASSWORD,
            to_file="reblogbot_usercred.txt"
        )
        self.account = self.pawoo.account_verify_credentials()

        self.followings = self.pawoo.account_following(self.account['id'])

        # self.path_following = config.get("file", "followings")
        #
        # try:
        #     with open(self.path_following) as f:
        #         self.followings = json.load(f)
        # except FileNotFoundError:
        #     self.followings = self.pawoo.account_following(self.account['id'])
        #     # with open(self.path_following, 'w') as f:
        #     #     json.dump(self.followings, f)
        #
        # print(self.followings)

        # print(self.account['id'])

    # def updateFolowing(self):
    #     following_ids = [following['id'] for following in self.pawoo.account_following(self.account['id'])]
    #     print(following_ids)
    #     pass

    def reblog(self):
        toots = self.pawoo.timeline_home(limit=80)
        for toot in toots:
            if toot['media_attachments']:
                self.pawoo.status_reblog(id=toot['id'])

    def unreblog(self):
        mytoots = self.pawoo.account_statuses(id=self.account['id'])
        for toot in mytoots:
            if toot['reblog']:
                self.pawoo.status_delete(id=toot['id'])

    # def hamafollow(self):
    #     # follows = self.pawoo.account_following(id=11338)
    #     # self.pawoo.ratelimit_limit = 100
    #     acc = self.pawoo.account_following(id=11338)
    #     # print(acc)
    #     # print(len(acc))
    #
    #     # follows = self.followings
    #
    #     self.pawoo.ratelimit_limit=80
    #
    #     for follow in acc:
    #         print('unfollow', follow['id'])
    #         # self.pawoo.account_follow(id=follow['id'])
    #     # print(len(follows))
    #     # # print(follows)
    #     # for follow in follows:
    #     #     tgtid = follow['id']
    #     #     print('followed', tgtid)
    #         try:
    #             # self.pawoo.account_unfollow(id=follow['id'])
    #             self.pawoo.account_follow(id=follow['id'])
    #         except:
    #             pass
    #     #     sleep(1)


if __name__ == '__main__':

    reblogbot = Bot()
    # reblogbot.hamafollow()

    reblogbot.reblog()
    # reblogbot.unreblog()
