#!/usr/bin/env python
#-*-coding: utf8-*-

import sys
import os
import re
import errno
import json

if not len(sys.argv) > 2:
    sys.exit(16)

infile = sys.argv[1]
regex = sys.argv[2]


try:
    statefile = sys.argv[3]
except:
    statefile = "log_state.json"

def open_file(filename, mode='r', ifnotexists=None):
    '''
    filename - path to file
    mode - mode to pass to open(), e.g. "r", "w", "r+" or "a"
    '''
    try:
        fp = open(filename, mode)
    except IOError as e:
        if e.errno == errno.ENOENT and ifnotexists=='create':
            if not os.path.exists(os.path.dirname(filename)):
                print "creating directory"
                try:
                    os.makedirs(os.path.abspath(os.path.dirname(filename)))
                except OSError as e:
                    if e.errno == 17:
                        pass
                    else:
                        raise
            fp = open(filename, 'w')
            fp.write('\n')
            fp.close()
            fp = open(filename, mode)
            return fp
        else:
            raise e
    else:
        return fp


def re_filter(line, regex):
    myre = re.compile(regex)
    if re.search(regex, line):
        return True
    else:
        return False


def get_full_path(filename):
    return os.path.abspath(filename)


def write_state_config(data, statefile):
    with open_file(statefile, 'w', 'create') as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4))
    return


def add_entry_to_data(path=infile,
                      regex=regex,
                      cur_date=0,
                      cur_size=0,
                      cur_byte=0,
                      firstline=''):
    for d in data:
        if d['path'] == path:
            d['state'].append({"date": cur_date,
                                "size": cur_size,
                                "byte": cur_byte,
                                "regex": regex,
                                "firstline": firstline})
            return data
    data.append({"path": path,
                "state":
                [
                    {"date": cur_date,
                    "size": cur_size,
                    "byte": cur_byte,
                    "regex": regex,
                    "firstline": firstline
                     }
                ]})
    return data

def update_entry(path=infile,
                 regex=regex,
                 cur_date=0,
                 cur_size=0,
                 cur_byte=0,
                 firstline=''):
    for d in data:
        if d['path'] == path:
            for r in d['state']:
                if r['regex'] == regex:
                    r["date"] = cur_date
                    r["byte"] = cur_byte
                    r["size"] = cur_size
                    r["firstline"] = firstline
                    return data
    return data


def read_state_config(statefile):
    with open_file(statefile,ifnotexists='create') as fp:
        mydata = json.load(fp)
    return mydata


def get_state(data, path, regex):
    for d in data:
        if d['path'] == path:
            for r in d['state']:
                if r['regex'] == regex:
                    return {'path': d['path'],
                            'state': r,
                        }
    return None

def get_firstline(infile):
    with open_file(infile,'r','create') as fp:
        return fp.readline()

def read_log_file(fp, regex, data):
    state = get_state(data, fp.name, regex)
    counter = 0
    fp.seek(state['state']['byte'])
    while True:
        line = fp.readline()
        if not line:
            break
        if re_filter(line, regex):
            counter += 1
    state = update_entry(fp.name, regex, cur_date, cur_size, firstline=firstline, cur_byte=fp.tell())
    print counter
    return state

infile = get_full_path(infile)

try:
    fp = open_file(infile, mode='r', ifnotexists='create')
except IOError:
    print u"I/O Error"
    sys.exit(1)

firstline = get_firstline(infile)
fp.seek(0)
cur_date = os.stat(infile).st_mtime
cur_size = os.stat(infile).st_size
cur_byte = 10

try:
    data = read_state_config(statefile)
except ValueError:
    data = [{'path': "", 'state': {'date': 0, 'size': 0, 'regex': 0, 'line': 0, 'firstline': ''}}]
    write_state_config(data, statefile)

state = get_state(data, infile, regex)

counter = 0

if state == None:
    data = add_entry_to_data(path=infile,
                      regex=regex,
                      cur_date=0,
                      cur_byte=0,
                      cur_size=0,
                      firstline='',
                      )
    state = get_state(data, infile, regex)


if (state['state']['size'] > cur_size) or (state['state']['firstline'] != firstline):
    update_entry(infile,regex,cur_date,cur_size,cur_byte=0, firstline=firstline)

with fp:
    data = read_log_file(fp, regex, data)
    write_state_config(data, statefile)