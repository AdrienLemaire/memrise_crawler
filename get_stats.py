#!/usr/bin/env python

import json
from itertools import izip_longest
import os
import sys


def format_status(status):
    if status not in ['now', 'not learnt']:
        status = ' '.join([str(e) for e in status])
    elif status == 'now':
        status = 'now\t'
    return status


def sort_status(el):
    """reduce to minutes and return that sort index"""
    if el[0] == "now\t":
        return 0
    if el[0] == "not learnt":
        return 10**10
    nb, text = el[0].split()

    minutes = {
        'day': 24*60,
        'days': 24*60,
        'hour': 60,
        'hours': 60,
        'minutes': 1,
        'seconds': 1.0/60,
    }
    return int(nb) * minutes[text]


def main(json_file):
    data = []
    stats = {}
    with open(json_file, 'r') as f:
        data = json.load(f)
    print "Number of questions: {}\n".format(len(data))

    #data = {d['course']: {d['item_id']: d['status']} for d in data}

    for d in data:
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
