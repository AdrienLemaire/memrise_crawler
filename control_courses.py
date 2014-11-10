#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script to get daily emails about changes on a course

  1. login
  2. Get courses id
  3. Get all levels id
  4. Get all items id
  5. Get all items details
  6. Compare the difference with last batch, and save difference

'''
import argparse
import json
from lxml import html
import math
import numpy as np
import os.path
import requests

from local_settings import USERNAME, PASSWORD


COURSES_ID = [351257, 351255]
DIFF_FILE = os.path.join('data', 'daily_diff.json')
ALL_DATA_FILE  = os.path.join('data', 'all_data.json')


def parse_args():
    parser = argparse.ArgumentParser(
        description='save all data and get difference')
    parser.add_argument('-d', action="store", dest='diff',
        default=DIFF_FILE, help='diff file')
    parser.add_argument('-a', action="store", dest='all',
        default=ALL_DATA_FILE, help='file to store all data')
    return parser.parse_args()


def main(diff_file, all_file):
    all_data = {
        'courses': [],
        'levels': [],
        'items': [],
    }
    with requests.Session() as s:
        url = "https://www.memrise.com/login/"
        s.get(url, verify=True)  # get cookies
        payload = {
            'username': USERNAME,
            'password': PASSWORD,
            'csrfmiddlewaretoken': s.cookies['csrftoken'],
        }
        s.post(url, data=payload, headers={'Referer': url})  # login
        for course_id in COURSES_ID:
            course_url = 'http://www.memrise.com/api/course/get/?course_id={}'
            rc = s.get(course_url.format(course_id))
            cdata = json.loads(rc.content)
            all_data['courses'].append(cdata)
            for level in cdata['course']['levels']:
                print "query level"
                level_url = 'http://www.memrise.com/api/level/get/?level_id={}'
                rl = s.get(level_url.format(level['id']))
                ldata = json.loads(rl.content)
                all_data['levels'].append(ldata)
                page = s.get('http://www.memrise.com{}'.format(
                    ldata['level']['url']))
                tree = html.fromstring(page.text)

                items_id = tree.xpath(
                    '//div[contains(@class, "thing")]/@data-thing-id')
                for item_id in items_id:
                    item_url = 'http://www.memrise.com/api/thing/get/?thing_id={}'
                    ri = s.get(item_url.format(item_id))
                    idata = json.loads(ri.content)
                    all_data['items'].append(idata)

        with open(all_file, 'w+') as f:
            f.write(json.dumps(all_data, indent=4))


if __name__ == '__main__':
    args = parse_args()
    main(args.diff, args.all)
