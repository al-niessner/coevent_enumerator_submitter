'''encapsulate all that it takes to get an orbit'''

import es.request

def load (acquisition:dict):
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


def test():
    '''simple unit test'''
    acq = {'id':'a-S1A_OPER_PREORB-b',
           'starttime':'2020-09-01T01:00:00Z',
           'endtime':'2020-09-01T02:00:00Z'}
    orb = load(acq)
    expected = 'S1A_OPER_AUX_POEORB_OPOD_20200921T121449_V20200831T225942'
    expected += '_20200902T005942-v1.1'
    if orb['id'] == expected: print ('preorb check passed')
    else: print ('preorb check FAILED')
    return
