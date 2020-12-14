#! /usr/bin/env python3
'''module that orchestrates all of the work
'''

import active
import datetime
import es
import es.request
import pprint
import time

def initialize (aoi):
    '''add state information that this processing needs

    Check the AOI for the state information. If it does not exist, then add it.
    '''
    if active.EP not in aoi:
        aoi[active.EP] = {
            'post':{'acqs':[], 'count':0, 'length':3, 'slcs':[],
                    active.TBIS:86400},
            'pre':{'acqs':[], 'count':0, 'length':3, 'slcs':[],
                   active.TBIS:86400},
            'previous':'',
            }
        td = datetime.timedelta(seconds=aoi[active.EP]['post']['time_blackout_in_seconds'])
        et = datetime.datetime.fromisoformat(aoi['metadata']['eventtime'][:-1])
        prev = et + td
        aoi[active.EP]['previous'] = prev.isoformat('T','seconds')+'Z'
        active.update (aoi)
        pass
    return

def main():
    '''the main processing block -- find and loop over all active AOIs'''
    time.sleep (300)
    for response in es.query (es.request.ALL_ACTIVE_AOI):
        aoi = response['_source']
        initialize (aoi)
        active.process (aoi)
        pprint.pprint (aoi, indent=2, width=120)
        pass
    return

if __name__ == '__main__': main()
