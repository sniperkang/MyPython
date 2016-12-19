# -*- coding: utf-8 -*-

import requests

BASE_URL = 'http://api.github.com'


def construct_url(end_point):
    return '/'.join([BASE_URL, end_point])


def basic_auth():
    """基本认证
    """
    response = requests.get(construct_url('user'), auth=('imoocdemo', 'imoocdemo123'))
    print response.text
    print response.request.headers

basic_auth()