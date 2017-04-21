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
            # ratelimit_method='pace',
            # ratelimit_pacefactor=2.0
        )

        self.pawoo.log_in(
            username=USERNAME,
            password=PASSWORD,
            to_file="reblogbot_usercred.txt"
        )
        self.account = self.pawoo.account_verify_credentials()

        self.followings = self.pawoo.account_following(self.account['id'])

        self.reblog_count = {}

        with open('reblogs.json') as f:
            self.reblog_count = json.load(f)

        self.reblog_queue = [key for key in self.reblog_count.keys()]

            # self.reblog_queue = [self.reblog_count.keys]






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


    def read_timeline_home(self):
        toots = self.pawoo.timeline_home()
        for toot in toots:
            if toot['reblog']:
                t = toot['reblog']
            else:
                t = toot
            # 誰かへのreplyは除く. 画像付き投稿を対象にする.
            if not t['in_reply_to_id'] and t['media_attachments']:
                self.reblog_queue.append(t['id'])


    def read_timeline_hashtag(self, hashtag=None):
        toots = self.pawoo.timeline_hashtag(hashtag=hashtag)
        for toot in toots:
            if toot['reblog']:
                t = toot['reblog']
            else:
                t = toot
            # 誰かへのreplyは除く. 画像付き投稿を対象にする.
            if not t['in_reply_to_id'] and t['media_attachments']:
                self.reblog_queue.append(t['id'])


    def reblog_toot(self):
        """
        キューに保存したtootをreblogする
        """
        FAVOURITES_THRESHOLD = 10
        REBLOGS_THRESHOLD = 10


        id = self.reblog_queue.pop(0)
        print(id)
        toot = self.pawoo.status(id)
        if toot['favourites_count'] >= FAVOURITES_THRESHOLD and toot['reblogs_count'] >= REBLOGS_THRESHOLD:
            pass
        else:
            return

        # 自分がreblogしたことがあれば解除
        if toot['reblogged']:
            self.pawoo.status_unreblog(id)

        self.pawoo.status_reblog(id)
        print('reblogged', id)

        # reblog回数を+1する
        self.reblog_count[str(id)] = self.reblog_count.get(str(id), 0) + 1

        # reblog結果回数を保存する
        with open('reblogs.json', 'w') as f:
            json.dump(self.reblog_count, f, indent=4)


if __name__ == '__main__':
    reblogbot = Bot()
    # reblogbot.hamafollow()

    reblogbot.read_timeline_home()
    # reblogbot.read_timeline_hashtag('水着')

    reblogbot.reblog_toot()
    # reblogbot.unreblog()

    while True:
        reblogbot.reblog_toot()
        sleep(5)
        # reblogbot.unreblog()
