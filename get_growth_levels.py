#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import json
import math
import requests

from local_settings import USERNAME, PASSWORD


def parse_args():
    parser = argparse.ArgumentParser(description='get growth levels')
    parser.add_argument('-i', action="store", dest='input',
        default='memrise_items.json', help='json file input')
    return parser.parse_args()


def main(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    items = [d['item_id'] for d in data]
    growth_levels = []
    with requests.Session() as s:
        url = "https://www.memrise.com/login/"
        s.get(url, verify=True)  # get cookies
        payload = {
            'username': USERNAME,
            'password': PASSWORD,
            'csrfmiddlewaretoken': s.cookies['csrftoken'],
        }
        s.post(url, data=payload, headers={'Referer': url})  # login

        for i in range(int(math.ceil(len(items)/438.0))):
            list_ids = ','.join(items[i*438:i*438+438])
            url = 'https://www.memrise.com/api/thing/stats/?thing_ids=[{}]'
            r = s.get(url.format(list_ids))
            data = json.loads(r.content)
            growth_levels += [d['growth_level'] for d in data['things']]

    print "List of my Memrise items levels"
    for i in range(min(growth_levels), max(growth_levels)):
        print "\t* level {}: {} items".format(i, growth_levels.count(i))



if __name__ == '__main__':
    args = parse_args()
    main(args.input)
