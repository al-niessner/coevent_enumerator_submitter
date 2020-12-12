'''module that orchestrates all of the work
'''

import active
import datetime
import es
import es.request
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
        time.sleep (300)
        pass
    return

def main():
    '''the main processing block -- find and loop over all active AOIs'''
    for response in es.query (es.request.ALL_ACTIVE_AOI):
        aoi = response['_source']
        initialize (aoi)
        print (aoi)
        active.process (aoi)
        pass
    return

if __name__ == '__main__': main()
