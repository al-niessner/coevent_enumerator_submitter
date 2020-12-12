'''module processes an active AOI

This is the bulk of the pseudo code in the README.md that is inside the
outermost loop. It was separated from iterate.py simply to make is trivial
to move it into its own job mechanism.
'''

import datetime
import es.request
import orbit
import slc

EP = 'event_processing'
TBIS = 'time_blackout_in_seconds'

def enough_coverage (aoi, acqs, version_mismatch=0):
    '''determine if these acquisitions (acqs) are good enough

    - Must determine how much of the AOI location is covered.
        - only care about land
        - any intersection is considered required
    - If all the acquisitions are processed with same version
    '''

    # use shapely for area problem
    return True

def fill (aoi):
    '''find all of the past acquisitions'''
    begin = datetime.datetime.fromisoformat (aoi['metadata']['eventtime'][:-1])
    begin = begin - datetime.timedelta (seconds=aoi[EP]['pre'][TBIS])
    repeat = datetime.timedelta(days=7)
    step = datetime.timedelta(days=5)
    while aoi[EP]['pre']['count'] < aoi[EP]['pre']['length']:
        acqs = intersection (begin=begin, end=begin+repeat,
                             location=aoi['location'])
        begin = begin + step

        if enough_coverage (aoi, acqs):
            slcs = [slc.load (acq) for acq in acqs]
            aoi[EP]['pre']['acqs'].extend ([a['_id'] for a in acqs])
            aoi[EP]['pre']['slcs'].extend (slcs)
            aoi[EP]['pre']['count'] += 1
            pass
        pass
    return

def intersection (begin, end, location):
    '''find the list of acquisitions that intersect with the

    begin : start time the aquisition must be within
    end : last time the acquisition must be within
    location : geographic area the acquisition must intersect with

    The center or largest group of them that have less than a day separating
    them should be the one returned. An error/warning message should be sent
    up if there is more than one cluster.
    '''
    data = es.query (es.request.collate_acquisitions(begin, end, location))
    return [d['_source'] for d in data]

def process (aoi):
    '''process the AOI as described by the pseudo code in README.md
    '''
    fill(aoi)
    begin = datetime.datetime.fromisoformat (aoi[EP]['previous'][:-1])
    acqs = intersection (begin=begin,
                         end=datetime.datetime.utcnow(),
                         location=aoi['location'])

    if enough_coverage (aoi, acqs):
        eofs = [orbit.load (acq) for acq in acqs + aoi[EP]['pre']['acqs']]
        slcs = [slc.load (acq) for acq in acqs]
        aoi[EP]['post']['acqs'].extend ([a['_id'] for a in acqs])
        aoi[EP]['post']['slcs'].extend ([s['_id'] for s in slcs])
        aoi[EP]['previous'] = datetime.datetime.utcnow().isoformat('T','seconds')+'Z'
        update (aoi)
        pass
    return

def update (aoi):
    '''write the AOI back out to ES

    Much of the AOI processing updates the the state information and it needs
    to be recorded in ES.
    '''
    return

def test_intersection():
    '''simple unit test'''
    begin = datetime.datetime(2020,9,1,0,0,0)
    end = datetime.datetime(2020,9,8,0,0,0)
    location = { 'type':'polygon',
                 'coordinates':[[[-118.60359191894533,34.163522648722825],
                                 [-118.60359191894533,34.27821226443234],
                                 [-118.4703826904297,34.27821226443234],
                                 [-118.4703826904297,34.163522648722825],
                                 [-118.60359191894533,34.163522648722825]]]}
    acqs = intersection (begin, end, location)
    if len(acqs) == 6652: print ('intersection test passed')
    else: print ('intersection test FAILED')

    starts = [datetime.datetime.fromisoformat (acq['starttime'][:-1]) < end
              for acq in acqs]
    ends = [begin < datetime.datetime.fromisoformat (acq['endtime'][:-1])
            for acq in acqs]
    if sum(starts) == len (starts): print ('intersection time passed')
    else: print ('intersection time FAILED')
    if sum(ends) == len (ends): print ('intersection time passed')
    else: print ('intersection time FAILED')
    return
