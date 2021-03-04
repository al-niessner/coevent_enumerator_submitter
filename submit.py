#! /usr/bin/env python3
'''Small script to allow coseismic enumerator to be run from cron'''

import json
import requests
import sys

job_params = {}
job_release = 'step_11'
job_type = 'job-enumerator'
queue = 'factotum-job_worker-coseismic-enumerator'
tag_name = 'coseismic-enumerator-cron'
params = {
    'queue': queue,
    'priority': '6',
    'job_name': job_type,
    'tags': tag_name,
    'type': "{}:{}".format(job_type, job_release),
    'params': json.dumps(job_params),
    'enable_dedup': False
}
req = requests.post(sys.argv[1], params=params, verify=False)
req.raise_for_status()
print(req.text)
print(req.json())
