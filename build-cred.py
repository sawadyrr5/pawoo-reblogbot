#!/usr/local/bin python
# -*- coding: utf-8 -*-
from mastodon import Mastodon
import configparser

INSTALL_PATH = '/hoge/app-path/'

config = configparser.ConfigParser()
config.read(INSTALL_PATH + 'config.ini')

API_BASE_URL = config.get("api", "API_BASE_URL")

# credentialを作る
Mastodon.create_app(
    "pawoo-reblogbot",
    api_base_url=API_BASE_URL,
    to_file="reblogbot_clientcred.txt"
)

mastodon = Mastodon(
    client_id="reblogbot_clientcred.txt",
    api_base_url=API_BASE_URL
)

mastodon.log_in(
    username='your_username',
    password='your_password',
    to_file="reblogbot_usercred.txt"
)
