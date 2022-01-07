#!/usr/bin/env python

# Copyright (C) 2015 Harvey Chapman <hchapman@3gfp.com>
# Public Domain
# Use at your own risk.

"""
Splits a gpx file with breaks in the track into separate files.

Based on: http://stackoverflow.com/q/33803614/47078
"""

import sys
import re
import os
from datetime import datetime, timedelta
#from itertools import izip
try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass
from xml.etree import ElementTree

ns = { 'gpx': 'http://www.topografix.com/GPX/1/1' }

def iso8601_to_datetime(datestring):
    d = datetime(*map(int, re.split('\D', datestring)[:-1]))
    # intentionally ignoring timezone info (for now)
    # d = d.replace(tzinfo=UTC)
    return d

def datetime_from_trkpt(trkpt):
    datestring = trkpt.find('gpx:time', ns).text
    return iso8601_to_datetime(datestring)
    
def delta_too_large(trkpt1, trkpt2):
    delta = datetime_from_trkpt(trkpt2) - datetime_from_trkpt(trkpt1)
    ##return delta > timedelta(seconds=2)
    return delta > timedelta(minutes=10)

def trkpt_groups(trkpts):
    last_index = 0
    for n, (a,b) in enumerate(zip(trkpts[:-1], trkpts[1:]), start=1):
        if delta_too_large(a,b):
            yield last_index, n
            last_index = n
    yield last_index, len(trkpts)

def remove_all_trkpts_from_trkseg(trkseg):
    trkpts = trkseg.findall('gpx:trkpt', ns)
    for trkpt in trkpts:
        trkseg.remove(trkpt)
    return trkpts

def add_trkpts_to_trkseg(trkseg, trkpts):
    # not sure if this will be slow or not...
    for trkpt in reversed(trkpts):
        trkseg.insert(0, trkpt)

def save_xml(filename, index, tree):
    filename_parts = os.path.splitext(filename)
    new_filename = '{1}_{0}{2}'.format(index, *filename_parts)
    ##with open(new_filename, 'wb') as f:
    ## path=os.getcwd()+file
    with open(os.getcwd()+'/'+os.path.splitext(filename)[0]+'/'+new_filename, 'wb') as f:
        tree.write(f,
                   xml_declaration=True,
                   encoding='utf-8',
                   method='xml')

def get_trkseg(tree):
    trk = tree.getroot().findall('gpx:trk', ns)
    if len(trk) > 1:
        raise Exception("Don't know how to parse multiple tracks!")
    trkseg = trk[0].findall('gpx:trkseg', ns)
    if len(trkseg) > 1:
        raise Exception("Don't know how to parse multiple track segment lists!")
    return trkseg[0]
    
def split_gpx_file(filename):
    ElementTree.register_namespace('', ns['gpx'])
    ## MY CODE
    ##print os.path.splitext(filename)[0]
    if not os.path.exists(os.path.splitext(filename)[0]):
         os.makedirs(os.path.splitext(filename)[0])
    ## MY CODE
    tree = ElementTree.parse(filename)
    trkseg = get_trkseg(tree)
    trkpts = remove_all_trkpts_from_trkseg(trkseg)
    for n, (start,end) in enumerate(trkpt_groups(trkpts)):
        # Remove all points and insert only the ones for this group
        remove_all_trkpts_from_trkseg(trkseg)
        add_trkpts_to_trkseg(trkseg, trkpts[start:end])
        save_xml(filename, n, tree)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: {} file.gpx".format(sys.argv[0])
        sys.exit(-1)
    split_gpx_file(sys.argv[1])
