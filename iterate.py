#! /usr/bin/env python3
'''module that orchestrates all of the work
'''

import active
import context
import datetime
import es
import es.request
import logging
import orbit
import traceback

logging.basicConfig(filename='enumerator.log')

def initialize (aoi):
    '''add state information that this processing needs

    Check the AOI for the state information. If it does not exist, then add it.
    '''
    if active.EP not in aoi:
        aoi[active.EP] = {
            active.CT:context.coverage_threshold_percent(),
            'post':{'acqs':[], 'count':0, 'length':context.post_count(),
                    active.TBIS:context.post_buffer_in_seconds()},
            'pre':{'acqs':[], 'count':0, 'length':context.prior_count(),
                   active.TBIS:context.prior_buffer_in_seconds()},
            'previous':'',
            }
        # pylint: disable=invalid-name
        dt = aoi[active.EP]['post']['time_blackout_in_seconds']
        dt = datetime.timedelta(seconds=dt)
        et = datetime.datetime.fromisoformat(aoi['metadata']['eventtime'][:-1])
        prev = et + dt
        # pylint: enable=invalid-name
        aoi[active.EP]['previous'] = prev.isoformat('T','seconds')+'Z'
        active.update (aoi)
        pass
    return

def main():
    '''the main processing block -- find and loop over all active AOIs'''
    for response in es.query (es.request.ALL_ACTIVE_AOI):
        aoi = response['_source']
        print ('begin:', aoi['id'])
        initialize (aoi)
        try: active.process (aoi)
        except orbit.NoOrbitsAvailable: traceback.print_last()
        print ('done:', aoi['id'])
        pass
    return

if __name__ == '__main__': main()
