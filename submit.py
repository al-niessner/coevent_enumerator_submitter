#! /usr/bin/env python3
'''Small script to allow coseismic enumerator to be run from cron'''

import json
import requests
import sys

job_params = [{"destination": "context",
               "name": "coverage_threshold_percent",
               "value": 90},
              {"destination": "context",
               "name": "post_count",
               "value": 3},
              {"destination": "context",
               "name": "post_buffer_in_seconds",
               "value": 60},
              {"destination": "context",
               "name": "prior_count",
               "value": 3},
              {"destination": "context",
               "name": "prior_buffer_in_seconds",
               "value": 60},
              {"destination": "context",
               "name": "reset_all",
               "value": 0}]
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
    'params': job_params,
    'enable_dedup': False
}
req = requests.post(sys.argv[1], params=params, verify=False)
req.raise_for_status()
print(req.text)
print(req.json())
