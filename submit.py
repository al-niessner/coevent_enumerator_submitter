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
tag_name = ['coseismic-enumerator-cron']
params = {
    'queue': queue,
    'priority': 6,
    'job_name': job_type,
    'tags': json.dumps(tag_name),
    'type': "{}:{}".format(job_type, job_release),
    'params': json.dumps(job_params),
    'enable_dedup': False
}
req = requests.post(sys.argv[1], params=params, verify=False)
req.raise_for_status()
print(req.text)
print(req.json())

# curl --insecure
#      -X POST https://100.67.33.56/mozart/api/v0.1/job/submit?
#                     queue=factotum-job_worker-coseismic-enumerator&
#                     priority=6&
#                     job_name=job-enumerator&
#                     tags=coseismic-enumerator-cron&
#                     type=job-enumerator%3Astep_11&
#                     params=%5B%7B%22destination%22%3A+%22context%22%2C+%22name%22%3A+%22coverage_threshold_percent%22%2C+%22value%22%3A+90%7D%2C+%7B%22destination%22%3A+%22context%22%2C+%22name%22%3A+%22post_count%22%2C+%22value%22%3A+3%7D%2C+%7B%22destination%22%3A+%22context%22%2C+%22name%22%3A+%22post_buffer_in_seconds%22%2C+%22value%22%3A+60%7D%2C+%7B%22destination%22%3A+%22context%22%2C+%22name%22%3A+%22prior_count%22%2C+%22value%22%3A+3%7D%2C+%7B%22destination%22%3A+%22context%22%2C+%22name%22%3A+%22prior_buffer_in_seconds%22%2C+%22value%22%3A+60%7D%2C+%7B%22destination%22%3A+%22context%22%2C+%22name%22%3A+%22reset_all%22%2C+%22value%22%3A+0%7D%5D&
#                     enable_dedup=False
#      -H "accept: application/json"
