'''transact with geo-data and satelite data'''

import json
import osgeo.ogr

def convert (acq, eof=None):
    '''convert an object with ['location'] to a shapely polygon'''
    poly = osgeo.ogr.CreateGeometryFromJson(json.dumps(acq['location']))

    # if an orbit file is given, the turn into footprint
    if eof:
        pass
    return poly

def coverage (aoi, acqs, eofs):
    '''compute the percentage of the coverage

    The acquisitions (acqs) need to be shifted to footprints via the orbit file
    then those footprints unioned and then intersected with the aoi['location'].

    The result is the area(intersection)/area(aoi['location'])*100
    '''
    fps = [convert (acq, eof) for acq,eof in zip(acqs,eofs)]
    whole_fp = union (fps)
    aoi_ = convert (aoi)
    intersection = aoi_.intersection (whole_fp)
    percent = intersection.area() / aoi_.area() * 100.
    return percent

def union (polys):
    '''Create the union of a list of shapely polygons'''
    result = polys[0]
    for poly in polys[1:]: result = result.Union (poly)
    return result
