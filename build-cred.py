#!/usr/local/bin python
# -*- coding: utf-8 -*-
from mastodon import Mastodon

API_BASE_URL = 'https://pawoo.net'
CLIENTCRED_FILE = 'reblogbot_clientcred.txt'
USERCRED_FILE = 'reblogbot_usercred.txt'

# credentialを作る
Mastodon.create_app(
    "pawoo-reblogbot",
    api_base_url=API_BASE_URL,
    to_file=CLIENTCRED_FILE
)

mastodon = Mastodon(
    client_id=CLIENTCRED_FILE,
    api_base_url=API_BASE_URL
)

mastodon.log_in(
    username='your_username',
    password='your_password',
    to_file=USERCRED_FILE
)
