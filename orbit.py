'''encapsulate all that it takes to get an orbit'''

import es.request
import isceobj.Sensor.TOPS.Sentinel1

def fetch (acquisition:dict):
    '''load orbit files of highest precision for given acquisition'''
    sat = acquisition['id'].split('-')[1].split('_')[0]
    orb = es.query (es.request.pair_acquisition_with_orbit
                    (acquisition['starttime'], acquisition['endtime']))
    mat = [o['_id'].startswith (sat) for o in orb]

    if not orb and not any(mat):
        orb = es.query (es.request.pair_acquisition_with_orbit
                        (acquisition['starttime'],acquisition['endtime'],True))
        mat = [o['_id'].startswith (sat) for o in orb]
        pass

    if not orb and not any(mat): raise RuntimeError('No orbits could be found')

    return orb[mat.index(True)]['_source']

def load (tstart, tend, orbit_file):
    '''Function that will extract the sentinel-1 state vector information

    from the orbit files and populate a ISCE sentinel-1 product with the state
    vector information.
    '''
    # initiate a Sentinel-1 product instance
    sentinel1 = isceobj.Sensor.TOPS.Sentinel1.Sentinel1()
    sentinel1.configure()
    sentinel1.orbitFile = orbit_file

    # ISCE internals read the required time-period to be extracted from the
    # orbit using the sentinel-1 product start and end-times.
    # Below we will add a dummy burst with the user-defined start and end-time
    # and include it in the sentinel-1 product object.

    print("Orbit File : %s" %orbit_file)
    # Create empty burst SLC
    burst = []
    burst1 = isceobj.Sensor.TOPS.BurstSLC.BurstSLC()
    burst1.configure()
    burst1.burstNumber = 1
    burst.append(burst1)

    # adding the start and end time
    burst[0].sensingStart=tstart
    burst[0].sensingStop=tend

    # add SLC burst to product
    sentinel1.product.bursts = burst

    # extract the precise orbit information into an orb variable
    orb = sentinel1.extractPreciseOrbit()

    # add the state vector information ot the burst SLC product
    for state_vector in orb: burst1.orbit.addStateVector(state_vector)
    return burst1

def test():
    '''simple unit test'''
    acq = {'id':'a-S1A_OPER_PREORB-b',
           'starttime':'2020-09-01T01:00:00Z',
           'endtime':'2020-09-01T02:00:00Z'}
    orb = fetch(acq)
    expected = 'S1A_OPER_AUX_POEORB_OPOD_20200921T121449_V20200831T225942'
    expected += '_20200902T005942-v1.1'
    if orb['id'] == expected: print ('preorb check passed')
    else: print ('preorb check FAILED')
    return
