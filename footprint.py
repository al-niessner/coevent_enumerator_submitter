'''transact with geo-data and satelite data'''

import isceobj
import json
import osgeo.ogr

def convert (acq, eof=None):
    '''convert an object with ['location'] to a shapely polygon'''
    if eof:
        poly = osgeo.ogr.CreateGeometryFromJson(json.dumps(acq['location']))
    else:  poly = osgeo.ogr.CreateGeometryFromJson(json.dumps(acq['location']))
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
    intersection = aoi_.Intersection (whole_fp)
    percent = intersection.Area() / aoi_.Area() * 100.
    print (aoi['id'],'coverage:',percent)
    return percent

def union (polys):
    '''Create the union of a list of shapely polygons'''
    result = polys[0]
    for poly in polys[1:]: result = result.Union (poly)
    return result

def topo (burst, time, Range, doppler=0, wvl=0.056):
    '''Function that return the lon lat information for a given
       time, range, and doppler'''
    ###Planet parameters
    elp = Planet(pname='Earth').ellipsoid

    # Provide a zero doppler polygon in case 0 is given
    if doppler is 0:
        doppler = Poly2D()
        doppler.initPoly(rangeOrder=1, azimuthOrder=0, coeffs=[[0, 0]])
        pass

    # compute the lonlat grid
    latlon = burst.orbit.rdr2geo (time, Range, doppler=doppler, wvl=wvl)
    return latlon

def get_plot_data (latlon_outline, satpath):
    from mpl_toolkits.basemap import Basemap
    mmap = Basemap(projection='cyl')
    lat, lon = mmap(latlon_outline[:,1], latlon_outline[:,0])
    latlon_outline=list(zip(lat,lon))
    #print("latlon_outline : %s" %latlon_outline)
    track_outline = Polygon( latlon_outline)
    #print("track_outline : %s" %track_outline)
    return latlon_outline

def get_ground_track (tstart, tend, mission, orbit_file):
    # generating an Sentinel-1 burst dummy file populated with state vector
    # information for the requested time-period
    burst = orbit(tstart,tend,mission,orbit_file, orbitDir)
    orbit_file = os.path.basename(orbit_file)
    print("groundTrack : get_ground_track: %s, %s, %s, %s "
          %(tstart, tend, mission, orbit_file))

    # constants for S1
    nearRange = 800e3 #Near range in m
    farRange = 950e3  #Far range in m
    doppler = 0       # zero doppler
    wvl = 0.056       # wavelength

    # sampling the ground swath (near and far range) in 10 samples
    latlon_nearR = []
    latlon_farR = []
    satpath = []
    #latlon_geoms = []
    delta = (tend - tstart).seconds
    print("delta : %s" %delta)
    #deltat = np.linspace(0,1, num=int(delta/2))
    deltat = np.linspace(0,1, num=delta)
    elp = Planet(pname='Earth').ellipsoid
    for tt in deltat:
        tinp = tstart + tt * (tend-tstart)
        latlon_nearR_pt = topo(burst,tinp,nearRange,doppler=doppler,wvl=wvl)
        #print("latlon_nearR_pt : %s " %latlon_nearR_pt)
        #latlon_nearR.append([latlon_nearR_pt[0], latlon_nearR_pt[1]])
        latlon_farR_pt = topo(burst,tinp,farRange,doppler=doppler,wvl=wvl)
        #latlon_farR.append([latlon_farR_pt[0], latlon_farR_pt[1]])
        #print("latlon_farR_pt : %s " %latlon_farR_pt)
        latlon_nearR.append(topo(burst,tinp,nearRange,doppler=doppler,wvl=wvl))
        latlon_farR.append(topo(burst,tinp,farRange,doppler=doppler,wvl=wvl))
        satpath.append(elp.xyz_to_llh(burst.orbit.interpolateOrbit(tinp, method='hermite').getPosition()))
        #latlon_geoms.append( [latlon_nearR_pt, latlon_farR_pt])
        pass
    latlon_nearR = np.array(latlon_nearR)
    latlon_farR = np.array(latlon_farR)
    satpath = np.array(satpath)
    # flip one side such that a polygon can be made by concatenating both.
    latlon_farR=np.flipud(latlon_farR)
    latlon_outline = np.vstack([latlon_nearR,latlon_farR])
    return get_plot_data(latlon_outline,satpath)
