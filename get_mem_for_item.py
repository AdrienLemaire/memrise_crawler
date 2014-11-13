#!/usr/bin/env python2
# -*- coding: utf-8 -*-


'''
Find your item id (by looking at your webpage source), and query as follow:

$ ./get_mem_for_item.py -i 41006508
http://www.memrise.com/mem/4321815/i-intend-to-become-a-lawyer/
$
'''

import argparse
import json
import os.path
import requests

from local_settings import USERNAME, PASSWORD


def parse_args():
    parser = argparse.ArgumentParser(description='get your mnemonic url for an item')
    parser.add_argument('-i', action="store", dest='item', help='item id')
    return parser.parse_args()


def main(item_id):
    with requests.Session() as s:
        # 1. login
        url = "https://www.memrise.com/login/"
        s.get(url, verify=True)  # get cookies
        payload = {
            'username': USERNAME,
            'password': PASSWORD,
            'csrfmiddlewaretoken': s.cookies['csrftoken'],
        }
        s.post(url, data=payload, headers={'Referer': url})

        # 2. get mems related to item
        url = "http://www.memrise.com/api/mem/get_many_for_thing/?thing_id={}"
        r = s.get(url.format(item_id))
        data = json.loads(r.content)
        my_mems = []
        for mem in data['mems']:
            if mem['author']['username'] == USERNAME:
                my_mems.append(mem['id'])

        # 3. get the url for my mems
        url = "http://www.memrise.com/api/mem/get/?mem_id={}"
        for mem_id in my_mems:
            r = s.get(url.format(mem_id))
            data = json.loads(r.content)
            print 'http://www.memrise.com{}'.format(data['mem']['absolute_url'])


if __name__ == '__main__':
    args = parse_args()
    main(args.item)
