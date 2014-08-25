#!/usr/bin/env python

import json
from itertools import izip_longest
import os
import sys

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
            course['nb_questions'] += 1
            if not status in course['time_left'].keys():
                course['time_left'][status] = 1
            else:
                course['time_left'][status] += 1

        # Total stats
        if d['status'] == 'now':
            total_stats['today'] += 1
        elif d['status'] == 'not learnt':
            total_stats['not learnt'] += 1
        elif 'minute' in d['status'][1]:
            total_stats['today'] += 1
        elif 'hour' in d['status'][1]:
            total_stats['today'] += 1
        elif d['status'][1] == 'day':
            total_stats['today'] += 1
        elif d['status'][1] == 'days' and 1 < d['status'][0] <= 7:
            total_stats['next week'] += 1
        elif d['status'][1] == 'days' and 7 < d['status'][0] <= 31:
            total_stats['next month'] += 1
        else:
            total_stats['long term'] += 1

    print "General stats:\n"
    #for key, nb in total_stats.iteritems():
        #print "\t{}: {} questions to review".format(key, nb)
    print "\tNumber of questions: {}".format(len(data))
    print "\tNb of reviews to do within a day: {}".format(total_stats['today'])
    print "\tOther reviews to do within 1 week: {}".format(total_stats['next week'])
    print "\tOther reviews to do within 1 month: {}".format(total_stats['next month'])
    print "\tOther reviews to do after 1 month: {}".format(total_stats['long term'])
    print "\tNb of questions not learnt: {}".format(total_stats['not learnt'])
    print "\n{}\n".format("~" * 80)

    # Save general stats in json file
    global_stats = {}
    with open(GENERAL_STATS_FILE, 'r') as f:
        global_stats = json.load(f)

    global_stats['yesterday'] = global_stats['today']
    global_stats['today'] = total_stats
    with open(GENERAL_STATS_FILE, 'w+') as f:
        f.write(json.dumps(global_stats, indent=4))

    messages = []
    for course, course_stats in stats.iteritems():
        message = [
            "Stats for {}".format(course),
            "Nb questions: {}".format(course_stats['nb_questions']),
        ]
        for t, nb in sorted(course_stats['time_left'].iteritems(), key=sort_status):
            message.append("\t{}: {}".format(t, nb))

        messages.append(message)

    print '\n'.join(['\t\t'.join(t) for t in izip_longest(*messages, fillvalue='\t\t')])

if __name__ == '__main__':
    json_file = 'memrise_items.json' if len(sys.argv) == 1 else sys.argv[1]
    main(json_file)
