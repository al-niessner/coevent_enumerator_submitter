'''module that orchestrates all of the work
'''

import aoi
import datetime
import es
import es.request

def initialize (data):
    '''add state information that this processing needs

    Check the AOI for the state information. If it does not exist, then add it.
    '''
    if 'event_processing' not in data:
        data['event_processing'] = {
            'post':{'acqs':[], 'count':0, 'slcs':[], 'threshold':3,
                    'time_blackout_in_seconds':86400},
            'pre':{'acqs':[], 'count':0, 'slcs':[], 'threshold':3,
                   'time_blackout_in_seconds':86400},
            'previous':'',
            }
        td = datetime.timedelta(seconds=data['event_processing']['post']['time_blackout_in_seconds'])
        et = datetime.datetime.fromisoformat(data['metadata']['eventtime'])
        prev = et + td
        data['event_processing']['previous'] = prev.isoformat('T','seconds')+'Z'
        aoi.update (data)
        pass
    return

def main():
    '''the main processing block -- find and loop over all active AOIs'''
    for response in es.query (es.request.ALL_ACTIVE_AOI):
        data = response['_source']
        initialize (data)
        print (data)
        aoi.process (data)
        pass
    return

if __name__ == '__main__': main()
