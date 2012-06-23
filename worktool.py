#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tool for time-based work@home
Author: Michał [balor] Thoma - http://balor.pl
'''


WORK_DAYS_PER_MONTH = 20
HOURS_PER_WORK_DAY = 8
CASH_PER_HOUR = 41.66
TAX_RATE = 1.09
FILENAME = './hours.txt'


from optparse import OptionParser

parser = OptionParser()
(options, params) = parser.parse_args()


def merge_str_list_from_index(data, index=0, mergechar=' '):
    if index >= len(data):
        return str()

    if index == len(data) - 1:
        return data[index]

    string = ''
    for x in range(index, len(data) - 1):
        if string != '':
            string += mergechar
        string += data[x]

    return string


def parse_hour_line(line):
    data = dict()
    chunks = line.split('-')

    if len(chunks) < 2:
        return None

    data['key'] = chunks[0].strip()
    try:
        data['hours'] = float(chunks[1].strip().split(' ')[0])
    except:
        print chunks[1].strip().split(' ')[0]

    if len(chunks) > 2:
        data['comment'] = merge_str_list_from_index(chunks, 2, '-')

    return data


def get_hours_data():
    if len(params) > 0:
        filename = params[0]
    else:
        filename = FILENAME

    try:
        f = open(filename)
    except IOError, e:
        print 'Can\'t open file {0}, I\'m dying.. :('.format(filename)
        exit()

    data = dict()
    last_cat = None
    for line in f:
        line = line.strip()

        if line.startswith('%'):
            line = line[1:]

            if not data.has_key(line):
                data[line] = dict()

            last_cat = line
        elif line:
            parsed_line = parse_hour_line(line)
            if parsed_line and last_cat:
                data[last_cat][parsed_line['key']] = parsed_line
    f.close()
    return data


def show_help():
    print '''
    Commands:
    clear - clear the screen
    exit - exit the program
    help - show availible commands
    hours [filter], cat [filter] - show hourtable
    ls - list all months
    sum [filter] - generate summary
    '''


def wildcardize(data, wildcard = None):
    if not wildcard or wildcard.strip() == '':
        return data

    trimmedData = dict()
    for (key, val) in data.items():
        key = key.lower()
        wildcard = wildcard.lower()
        if key.find(wildcard) != -1:
            trimmedData[key] = val

    return trimmedData


def show_hour_table(filter = None):
    hours = wildcardize(get_hours_data(), filter)
    for (key, val) in hours.items():
        print '\n\n{0}'.format(key)
        print '----------------'
        for (hkey, hval) in val.items():
            print '  {0} = {1} hours'.format(hkey, hval['hours'])
            if hval.has_key('comment'):
                print '    Comment: {0}'.format(hval['comment'])


def generate_summaries(filter = None):
    hours = wildcardize(get_hours_data(), filter)
    for (key, val) in hours.items():
        print '\n{0}\n----------------'.format(key)

        day_num = 0
        hours_worked = 0.0
        for (hkey, hval) in val.items():
            day_num += 1
            hours_worked += hval['hours']

        print 'Days worked: {0}/{1}'.format(
            day_num, WORK_DAYS_PER_MONTH)
        print 'Hours worked: {0}/{1}'.format(
            hours_worked, WORK_DAYS_PER_MONTH * HOURS_PER_WORK_DAY)
        print 'Average hours per day: {0} hours'.format(
            round(hours_worked / float(day_num), 2))
        print 'Average hours per working day: {0} hours'.format(
            round(hours_worked / float(WORK_DAYS_PER_MONTH), 2))
        cash_gross = hours_worked * CASH_PER_HOUR
        print 'Cash for the work: {0} PLN (gross)'.format(
            round(cash_gross, 2))
        print '                   {0} PLN (net)'.format(
            round(cash_gross / TAX_RATE, 2))
        print ''


def list_months():
    hours = get_hours_data()
    print '\n'
    for (key, val) in hours.items():
        print key + '\n'


def end_program():
    print '\n\nBye bye..'
    exit(0)


def clear_screen():
    print 80*'\n'


print '''Welcome to WorkTOOL
type `help` to show availible commands\n'''

actions = {
    'exit': end_program,
    'help': show_help,
    'hours': show_hour_table,
    'cat': show_hour_table,
    'sum': generate_summaries,
    'clear': clear_screen,
    'ls': list_months,
}

while True:
    try:
        command = raw_input('> ')
    except (Exception, KeyboardInterrupt):
        actions['exit']()

    chunks = command.split(' ')
    command = chunks[0]
    args = chunks[1:]

    try:
        actions[command](*args)
    except (TypeError, KeyError):
        print 'Unknown command :<'

