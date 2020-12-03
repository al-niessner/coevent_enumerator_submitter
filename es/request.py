'''module to hold the Elastic-Search query objects

Rather than pollute the code with the query information, hide them behind
a variable name.
'''

import datetime
import json

# the dataset will need to change
all_active_aoi = json.loads('''
{
  "bool": {
    "must": [
      {
        "term": {
          "dataset.raw": "S1-GUNW-AOI_TRACK"
        }
      },
      {
        "range": {
          "endtime": {
            "gt": "{0}Z"
          }
        }
      }
    ]
  }
}'''.format (datetime.datetime.utcnow().isoformat(timespec='seconds')))
