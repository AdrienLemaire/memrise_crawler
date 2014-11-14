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
from shutil import copyfile
from sendmail import sendMail
try:
    from local_settings import USERNAME, PASSWORD
except:
    import warnings
    warnings.warn('Please create a local_settings.py file')




COURSES_ID = [351257, 351255]
DIFF_FILE = os.path.join('data', 'daily_diff.json')
NEW_DATA_FILE  = os.path.join('data', 'all_data_new.json')
OLD_DATA_FILE  = os.path.join('data', 'all_data_old.json')


def parse_args():
    parser = argparse.ArgumentParser(
        description='save all data and get difference')
    parser.add_argument('-d', action="store", dest='diff',
        default=DIFF_FILE, help='diff file')
    parser.add_argument('-a', action="store", dest='all',
        default=NEW_DATA_FILE, help='file to store all data')
    parser.add_argument('-n', action="store_true", dest='noquery',
        help='do not query memrise and use the existing output file instead')
    return parser.parse_args()


def query_api():
    new_data = {
        'courses': {},
        'levels': {},
        'items': {},
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
            print "query course", course_id
            course_url = 'http://www.memrise.com/api/course/get/?course_id={}'
            rc = s.get(course_url.format(course_id))
            cdata = json.loads(rc.content)
            new_data['courses'][course_id] = cdata
            for level in cdata['course']['levels']:
                print "query level", level['id']
                level_url = 'http://www.memrise.com/api/level/get/?level_id={}'
                rl = s.get(level_url.format(level['id']))
                ldata = json.loads(rl.content)
                new_data['levels'][level['id']] = ldata
                page = s.get('http://www.memrise.com{}'.format(
                    ldata['level']['url']))
                tree = html.fromstring(page.text)

                items_id = tree.xpath(
                    '//div[contains(@class, "thing")]/@data-thing-id')
                for item_id in items_id:
                    item_url = 'http://www.memrise.com/api/thing/get/?thing_id={}'
                    ri = s.get(item_url.format(item_id))
                    idata = json.loads(ri.content)
                    new_data['items'][item_id] = idata
    with open(new_file, 'w+') as f:
        f.write(json.dumps(new_data, indent=4))


def main(diff_file, new_file, noquery):
    # Load old data
    with open(OLD_DATA_FILE, 'r') as f:
        old_data = json.load(f)

    # Load new data
    if noquery:
        with open(new_file, 'r') as f:
            new_data = json.load(f)
    else:
        # Copy previous backup to old data
        copyfile(new_file, OLD_DATA_FILE)
        # Build new backup
        new_data = query_api(new_file)

    # Report of activity
    message = ''

    # New words
    items_id = set(old_data['items'].keys()) ^ set(new_data['items'].keys())
    if items_id:
        message += u"<h1>New words added:</h1><ul>"
    for i in list(items_id):
        item = new_data['items'][i]['thing']['columns']
        if len(item.keys()) == 3:
            message += u'<li>{}（{}）: {}</li>'.format(item['1']['val'],
            item['3']['val'], item['2']['val'])
        elif len(item.keys()) == 5:
            message += u'<li>{}（{}）: {}</li>'.format(item['1']['val'],
            item['6']['val'], item['5']['val'])
    if items_id:
       message += '</ul>'

    # words changed
    if old_data['items'] != new_data['items']:
        message += u"<h1>Words modified:</h1><ul>"
    for i in list(set(new_data['items'].keys()) - items_id):
        col1 = old_data['items'][i]['thing']['columns']
        col2 = new_data['items'][i]['thing']['columns']
        att1 = old_data['items'][i]['thing']['attributes']
        att2 = new_data['items'][i]['thing']['attributes']
        if att1 != att2 or col1 != col2:
            message += u'<li>Item {} ({}) has changed!</li>'.format(i,
                col1['1']['val'])
        if att1 != att2:
            message += '<br />Different attributes: '
            message += '<br />'.join([u' → '.join([att1[k]['val'], att2[k]['val']])
                for k in att1.keys() if att1[k]['val'] != att2[k]['val']])
        if col1 != col2:
            for k in col1.keys():
                if col1[k]['alts'] != col2[k]['alts']:
                    message += '<br />New alts:</b> '
                    message += ','.join(set([d['val'] for d in
                        col1[k]['alts']]) .symmetric_difference(
                        set([d['val'] for d in col2[k]['alts']])))
                if col1[k]['val'] != col2[k]['val']:
                    message += '<br />Different val:</b> '
                    message += u' → '.join([col1[k]['val'], col2[k]['val']])
    if old_data['items'] != new_data['items']:
        message += '</ul>'
    sendMail(message)


if __name__ == '__main__':
    args = parse_args()
    main(args.diff, args.all, args.noquery)
