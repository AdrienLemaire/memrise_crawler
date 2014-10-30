#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import json
import math
import os.path
import requests

from local_settings import USERNAME, PASSWORD

INPUT_FILE = os.path.join('/tmp', 'memrise_items.json')
ALL_ITEMS_FILE = os.path.join(
    os.path.dirname(__file__),
    '..', 'kanji_learnt.github.io',
    'data', 'memrise_all_items.json')


def parse_args():
    parser = argparse.ArgumentParser(description='get growth levels')
    parser.add_argument('-i', action="store", dest='input',
        default=INPUT_FILE, help='json file input (to get items ids)')
    parser.add_argument('-o', action="store", dest='output',
        default=ALL_ITEMS_FILE, help='json file output (to store items data)')
    return parser.parse_args()


def main(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    items = [d['item_id'] for d in data]
    growth_levels = []
    all_data = []
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
            all_data += data['things']
            growth_levels += [d['growth_level'] for d in data['things']]

    with open(output_file, 'w+') as f:
        f.write(json.dumps(all_data, indent=4))

    print "List of my Memrise items levels"
    for i in range(min(growth_levels), max(growth_levels)):
        print "\t* level {}: {} items".format(i, growth_levels.count(i))



if __name__ == '__main__':
    args = parse_args()
    main(args.input, args.output)
