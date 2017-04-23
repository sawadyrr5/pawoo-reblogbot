# -*- coding: utf-8 -*-
from mastodon import Mastodon
import json
from datetime import datetime
import dateutil.parser
import random

INSTALL_PATH = '/hoge/'
CLIENTCRED_FILE = 'reblogbot_clientcred.txt'
USERCRED_FILE = 'reblogbot_usercred.txt'

API_BASE_URL = 'https://pawoo.net'

# reblogするtootのidとreblog回数を保存するファイル
FILE_REBLOGS = INSTALL_PATH + 'reblogs.json'


class Bot:
    def __init__(self):
        self.pawoo = Mastodon(
            client_id=INSTALL_PATH + CLIENTCRED_FILE,
            access_token=INSTALL_PATH + USERCRED_FILE,
            api_base_url=API_BASE_URL
        )
        self.account = self.pawoo.account_verify_credentials()

        # reblog対象toot idを読み込む
        self.reblog_count = {}
        with open(FILE_REBLOGS) as f:
            self.reblog_count = json.load(f)

    def read_timeline(self):
        toots = self.pawoo.timeline_home()
        for toot in toots:
            if toot['reblog']:
                t = toot['reblog']
            else:
                t = toot

            # replyは除く. 画像付き投稿を対象にする.
            if not t['in_reply_to_id'] and t['media_attachments']:
                if not t['id'] in self.reblog_count:
                    self.reblog_count.update({str(t['id']): 0})
        return

    def reblog_toot(self):
        """
        reblog queued toot
        """
        MAX_REBLOG_COUNT = 5
        REBLOGS = 5

        # 指定回数繰り返す
        for i in range(0, REBLOGS):
            id = random.choice(list(self.reblog_count.keys()))
            toot = self.pawoo.status(id)

            # tootがreblog条件を満たしており、自分がreblogした回数が規定の最大値以下であればreblogする
            if self._can_reblog(toot) and self.reblog_count[str(id)] < MAX_REBLOG_COUNT:

                # 自分がreblogしたことがあれば解除する
                if toot['reblogged']:
                    self.pawoo.status_unreblog(id)

                self.pawoo.status_reblog(id)

                # reblog回数を+1する
                self.reblog_count[str(id)] = self.reblog_count.get(str(id), 0) + 1

                # reblog結果回数を保存する
                with open(FILE_REBLOGS, 'w') as f:
                    json.dump(self.reblog_count, f, indent=4)

        return

    def _can_reblog(self, toot):
        FAVOURITES_THRESHOLD = 10
        REBLOGS_THRESHOLD = 10
        CREATED_TIME_THRESHOLD = 86400

        # 投稿から規定の時間が経過したものはreblogしない
        if datetime.now().timestamp() > dateutil.parser.parse(toot['created_at']).timestamp() + CREATED_TIME_THRESHOLD:
            return False

        # reblogとfavが規定回数に達していればreblogする
        if toot['favourites_count'] >= FAVOURITES_THRESHOLD and toot['reblogs_count'] >= REBLOGS_THRESHOLD:
            return True


if __name__ == '__main__':
    reblogbot = Bot()
    reblogbot.read_timeline()
    reblogbot.reblog_toot()
