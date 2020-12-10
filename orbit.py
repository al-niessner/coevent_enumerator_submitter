'''encapsulate all that it takes to get an orbit'''

import es.request

def load (acquisition):
    '''load orbit files of highest precision for given acquisition'''
    orb = es.query (es.request.pair_acquisition_with_orbit
                    (acquisition['starttime'], acquisition['endtime']))

    if not orb:
        orb = es.query (es.request.pair_acquisition_with_orbit
                        (acquisition['starttime'],acquisition['endtime'],True))
        pass

    if not orb: raise RuntimeError('No orbits could be found')
    return orb[0]['_source']
