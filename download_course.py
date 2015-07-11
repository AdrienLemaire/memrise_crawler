#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Download a full course as json
'''
import argparse
import json
from lxml import html
import os.path
import requests
try:
    from local_settings import USERNAME, PASSWORD
except:
    import warnings
    warnings.warn('Please create a local_settings.py file')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download a course')
    parser.add_argument('-c', action="store", dest='course',
        help='Course id (you can find it in the url of the course)')
    return parser.parse_args()


def main(course_id):
    output_file = os.path.join('data', '{}.json'.format(course_id))
    with requests.Session() as s:
        url = "https://www.memrise.com/login/"
        s.get(url, verify=True)  # get cookies
        payload = {
            'username': USERNAME,
            'password': PASSWORD,
            'csrfmiddlewaretoken': s.cookies['csrftoken'],
        }
        s.post(url, data=payload, headers={'Referer': url})  # login
        course_url = 'http://www.memrise.com/api/course/get/?course_id={}'
        rc = s.get(course_url.format(course_id))
        cdata = json.loads(rc.content)
    with open(output_file, 'w+') as f:
        f.write(json.dumps(cdata, indent=4))

    print "Data saved in {}".format(output_file)
    


if __name__ == '__main__':
    args = parse_args()
    main(args.course)
