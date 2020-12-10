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
pylint -d C0321,C0326,C0411,W0107,R1711 active.py iterate.py orbit.py slc.py es
```

### Latest Result
```
************* Module active
active.py:16:21: W0613: Unused argument 'aoi' (unused-argument)
active.py:16:26: W0613: Unused argument 'acqs' (unused-argument)
active.py:16:32: W0613: Unused argument 'version_mismatch' (unused-argument)
active.py:68:8: W0612: Unused variable 'eofs' (unused-variable)
active.py:69:8: W0612: Unused variable 'slcs' (unused-variable)
active.py:75:12: W0613: Unused argument 'aoi' (unused-argument)
************* Module iterate
iterate.py:22:8: C0103: Variable name "td" doesn't conform to snake_case naming style (invalid-name)
iterate.py:23:8: C0103: Variable name "et" doesn't conform to snake_case naming style (invalid-name)
************* Module orbit
orbit.py:1:0: C0114: Missing module docstring (missing-module-docstring)
orbit.py:2:10: W0613: Unused argument 'acquisition' (unused-argument)
************* Module slc
slc.py:1:0: C0114: Missing module docstring (missing-module-docstring)
slc.py:2:10: W0613: Unused argument 'acquisition' (unused-argument)
************* Module es
es/__init__.py:23:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
es/__init__.py:23:0: W0102: Dangerous default value {} as argument (dangerous-default-value)
es/__init__.py:23:0: R0913: Too many arguments (6/5) (too-many-arguments)

------------------------------------------------------------------
Your code has been rated at 8.66/10 (previous run: 8.30/10, +0.36)
```
