# -*- coding: utf -*-

import requests

def download_image():
    """demo下载图片
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    url = "http://image.lxway.com/upload/0/b2/0b2b7eb5ce674e66c6a728e85afae0f3_thumb.jpg"
    response = requests.get(url, headers=headers, stream=True)
    with open('demo.jpg', 'wb') as fd:
        for chunk in response.iter_content(128):
            fd.write(chunk)
    #print response.status_code, response.reason
    #print response.headers
    #print response.content


def download_image_improved():
    """demo下载图片
    """
    # 伪造headers信息
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    # 限定url
    url = "http://image.lxway.com/upload/0/b2/0b2b7eb5ce674e66c6a728e85afae0f3_thumb.jpg"
    response = requests.get(url, headers=headers, stream=True)
    from contextlib import closing
    with closing(requests.get(url, headers=headers, stream=True)) as response:
        #打开文件
        with open('demo1.jpg', 'wb') as fd:
        #每128写入一次
            for chunk in response.iter_content(128):
                fd.write(chunk)


download_image_improved()