# Co-Event Enumerator Submitter

Iterates through orbit an determining the relevant co-event AOIs overlaps, then submits enumeration jobs for the matching tracks and AOI.

## Outline of what it does

In a pseudo python form:

```
for aoi in get_active_aoitrack_datasets():

    n = 0

    while aoi['event']['pre']['count'] < aoi['event']['pre']['threshold']:

        acqs = list_of_acquisitions_intersecting(begin=aoi['eventtime'] - (n+1)*6days, end=aoi['event']['time'] - n*6days, location=aoi['location'])


        if enough_coverage (aoi, acqs):

            slcs = load_slcs (acqs)  # should shortcut to nothing because they exist?

            aoi['event']['pre']['acqs'].extend (acqs)

            aoi['event']['pre']['slcs'].extend (slcs)

            aoi['event']['pre']['count'] += 1

            pass


        n += 1

        pass

    acqs = list_of_acquisitions_intersecting (begin=aoi['previous'], end=utcnow(), location=aoi['location'])


    if not enough_coverage (aoi, acqs): exit  # need to define when there is enough coverage to include bad acqs


    eofs = load_orbits (aoi['pre-event']['acqs'] + acqs)

    slcs = load_slcs (acqs)  # this may shuffle it off to a different queue for other jobs to do

    do_coseisemic (aoi, acqs, eofs, slcs) 
    aoi['previous'] = utcnow()
    save_aoi_to_es (aoi)

do_coseisemic (aoi, acqs, eofs, slcs):
    '''use the name/url to build job information then put it in a queue to spawn the job

      if spawn job is successful it must:
         aoitrack['event']['post']['count'] += 1
         if aoitrack['event']['post']['threshold'] <= aoitrack['post-event']['count']: aoitrack['endtime'] = utcnow()
    '''
```

## Some static analysis

### Tool
```
pylint --version
pylint 2.4.4
astroid 2.3.3
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0]
```

### Command
```
pylint -d C0321,C0326,C0411,W0107,R1711 active.py iterate.py orbit.py slc.py test.py es
```

### Latest Result
```
************* Module active
active.py:20:2: W0511: FIXME: need to actually forard the information (fixme)
active.py:35:2: W0511: FIXME: use shapely for area problem (fixme)
active.py:126:2: W0511: FIXME: need to update AOI in ES (fixme)
active.py:23:21: W0613: Unused argument 'aoi' (unused-argument)
************* Module slc
slc.py:8:2: W0511: FIXME: need more here to start the localization process (fixme)

------------------------------------------------------------------
Your code has been rated at 9.74/10 (previous run: 9.69/10, +0.05)
```
