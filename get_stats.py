#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date
import json
from itertools import izip_longest
import os
import sys

from colorama import init, Fore
init()

GENERAL_STATS_FILE = os.path.join(
    os.path.dirname(__file__),
    '..', 'kanji_learnt.github.io',
    'data', 'memrise_global_stats.json')


def format_status(status):
    if status not in ['now', 'not learnt']:
        status = ' '.join([str(e) for e in status])
    elif status == 'now':
        status = 'now\t'
    elif status == '1 days':
        status = '1 day'
    elif status == '1 hours':
        status = '1 hour'
    return status


def sort_status(el):
    """reduce to minutes and return that sort index"""
    if el[0] == "now\t":
        return 0
    if el[0] == "not learnt":
        return 10**10
    nb, text = el[0].split()

    minutes = {
        'days': 24*60,
        'day': 24*60,
        'hours': 60,
        'hour': 60,
        'minutes': 1,
        'minute': 1,
        'seconds': 1.0/60,
    }
    return int(nb) * minutes[text]


def main(json_file):
    data = []
    stats = {}
    total_stats = {
        'today': 0,
        'next week': 0,
        'next month': 0,
        'long term': 0,
        'star': 0,
        'not learnt': 0,
    }
    with open(json_file, 'r') as f:
        data = json.load(f)

    #data = {d['course']: {d['item_id']: d['status']} for d in data}

    for d in data:
        # Course stats
        if not d['course'] in stats:
            stats[d['course']] = {
                'nb_questions': 1,
                'time_left': {format_status(d['status']): 1}
            }
        else:
            course = stats[d['course']]
            status = format_status(d['status'])
            if status == "1 hours":
                status = "1 hour"
            elif status == "1 days":
                status = "1 day"

            course['nb_questions'] += 1
            if not status in course['time_left'].keys():
                course['time_left'][status] = 1
            else:
                course['time_left'][status] += 1

        # Total stats
        now = datetime.now()
        if d['status'] == 'now':
            total_stats['today'] += 1
        elif 'second' in d['status'][1]:
            total_stats['today'] += 1
        elif 'minute' in d['status'][1]:
            if now.hour == 23 and (d['status'][0] > 60 - now.minute):
                total_stats['next week'] += 1
            else:
                total_stats['today'] += 1
        elif 'hour' in d['status'][1]:
            if d['status'][0] > 24 - now.hour:
                total_stats['next week'] += 1
            else:
                total_stats['today'] += 1
        elif d['status'][1] == 'day' or d['status'] == [1, 'days']:
            total_stats['next week'] += 1
        elif d['status'] == 'not learnt':
            total_stats['not learnt'] += 1
        elif d['status'][1] == 'days' and 1 < d['status'][0] <= 7:
            total_stats['next week'] += 1
        elif d['status'][1] == 'days' and 7 < d['status'][0] <= 31:
            total_stats['next month'] += 1
        elif d['status'][1] == 'days' and 31 < d['status'][0] <= 89:
            total_stats['long term'] += 1
        else:
            total_stats['star'] += 1


    pre = "\t{}".format(Fore.GREEN)
    pre_star = "\t{}".format(Fore.YELLOW)
    print "General stats:\n"
    #for key, nb in total_stats.iteritems():
        #print "\t{}: {} questions to review".format(key, nb)
    print "{}Number of questions: {}".format(pre, len(data))
    print "{}Nb of reviews left for today: {}".format(pre, total_stats['today'])
    print "{}Other reviews to do within 1 week: {}".format(pre, total_stats['next week'])
    print "{}Other reviews to do within 1 month: {}".format(pre, total_stats['next month'])
    print "{}Other reviews to do after 1 month: {}".format(pre, total_stats['long term'])
    print "{}★★★ 3+ months (perfect): {} ★★★".format(pre_star, total_stats['star'])
    print "{}Nb of questions not learnt: {}".format(pre, total_stats['not learnt'])
    print "\n{}\n".format("~" * 80)
    print Fore.RESET

    # Save general stats in json file
    global_stats = {}
    with open(GENERAL_STATS_FILE, 'r') as f:
        global_stats = json.load(f)

    global_stats[date.today().isoformat()] = total_stats
    with open(GENERAL_STATS_FILE, 'w+') as f:
        f.write(json.dumps(global_stats, indent=4))

    messages = []
    for course, course_stats in stats.iteritems():
        message = [
            "{}Stats for {}".format(Fore.BLUE, course),
            "{}Nb questions: {}{}".format(
                Fore.RESET,
                Fore.GREEN,
                course_stats['nb_questions'],
            ),
        ]
        for t, nb in sorted(course_stats['time_left'].iteritems(), key=sort_status):
            message.append("\t{}{}: {}".format({
                    'second': Fore.RED,
                    'minute': Fore.RED,
                    'learnt': Fore.MAGENTA,
                    'hour': Fore.YELLOW,
                    'day': Fore.CYAN,
                }[t.split()[1].rstrip('s') if ' ' in t else 'learnt'],
                t, nb))

        messages.append(message)

    print '\n'.join(['\t\t'.join(t) for t in izip_longest(*messages, fillvalue='\t\t')])

if __name__ == '__main__':
    json_file = 'memrise_items.json' if len(sys.argv) == 1 else sys.argv[1]
    main(json_file)
