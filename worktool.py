#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Tool for tine-based work@home
Author: Michał [balor] Thoma - http://balor.pl
'''

from optparse import OptionParser

parser = OptionParser()
(options, params) = parser.parse_args()

def mergeStrListFromIndex(data, index = 0, mergechar = ' '):
    if index >= len(data):
        return str()
    if index == len(data)-1:
        return data[index]
    string = ''
    for x in range(index, len(data)-1):
        if string != '':
            string += mergechar
        string += data[x]
    return string

def parseHourLine(line):
    data = dict()
    chunks = line.split('-')
    if len(chunks) < 2:
        return None

    data['key'] = chunks[0].strip()
    data['hours'] = chunks[1].strip().split(' ')[0]
    if len(chunks) > 2:
        data['comment'] = mergeStrListFromIndex(chunks, 2, '-')

    return data

def getHoursData():
    filename = 'hours.txt'
    if len(params) > 0:
        filename = params[0]
    try:
        f = open(filename)
    except IOError, e:
        print 'Can\' open file %s, I\'m dying.. :(' % filename
        exit()

    data = dict()
    lastCat = None
    for line in f:
        line = line.strip()
        if line.startswith('%'):
            line = line[1:]
            if not data.has_key(line):
                data[line] = dict()
            lastCat = line
        elif line != '':
            parsedLine = parseHourLine(line)
            if parsedLine and lastCat:
                data[lastCat][parsedLine['key']] = parsedLine
    f.close()
    return data

def showHelp():
    print '\nCommands:'
    print 'clear - clear the screen'
    print 'exit - exit the program'
    print 'help - show availible commands'
    print 'hours [filter] - show hourtable'
    print 'ls - list all months'
    print 'quit - exit the program'
    print 'sum [filter] - generate summary'
    print ''

def wildcardize(data, wildcard = None):
    if not wildcard or wildcard.strip() == '':
        return data
    trimmedData = dict()
    for (key, val) in data.items():
        if key.find(wildcard) != -1:
            trimmedData[key] = val
    return trimmedData

def showHourTable(filter = None):
    hours = wildcardize(getHoursData(), filter)
    for (key, val) in hours.items():
        print '\n\n' + key
        print '----------------'
        for (hkey, hval) in val.items():
            print '  %s = %s hours' % (hkey, hval['hours'])
            if hval.has_key('comment'):
                print '    Comment: ' + hval['comment']

def generateSummaries(filter = None):
    #TODO: should be in config file!!
    monthlyWorkDays = 20
    hoursPerDay = 6
    paymentPerHour = 41.66

    hours = wildcardize(getHoursData(), filter)
    for (key, val) in hours.items():
        print '\n' + key
        print '----------------'
        dayNum = 0
        hoursWorked = 0
        for (hkey, hval) in val.items():
            dayNum += 1
            if hval['hours'].isdigit():
                hoursWorked += int(hval['hours'])
        print 'Days worked: %s/%s' % (dayNum, monthlyWorkDays)
        print 'Hours worked: %s/%s' % (hoursWorked, (monthlyWorkDays * hoursPerDay))
        print 'Average hours per day: %s hours' % round(hoursWorked/dayNum, 2)
        print 'Average hours per month working day: %s hours' % round(hoursWorked/monthlyWorkDays, 2)
        print 'Cash for the work: %s PLN' % round(hoursWorked*paymentPerHour)
        print ''

def listMonths():
    hours = getHoursData()
    print '\n'
    for (key, val) in hours.items():
        print key + '\n'

def endProgram():
    print '\n\nBye bye..'
    exit()

print 'Welcome to WorkTOOL\n'
print 'type help to show availible commands\n'

programRunning = True
while (programRunning):
    try:
        command = raw_input('> ')
    except Exception, e:
        endProgram()
    except KeyboardInterrupt, e:
        endProgram()

    chunks = command.split(' ')
    command = chunks[0]
    param = None
    if (len(chunks) > 1):
        param = chunks[1]

    if command in ('quit', 'exit'):
        endProgram()
    elif command == 'help':
        showHelp()
    elif command == 'hours':
        showHourTable(param)
    elif command == 'sum':
        generateSummaries(param)
    elif command == 'clear':
        print 200 * '\n'
    elif command == 'ls':
        listMonths()
    else:
        print 'Unknown command :S'

