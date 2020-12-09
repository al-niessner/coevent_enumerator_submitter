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
          "dataset_type.raw": "area_of_interest"
        }
      },
      {
        "term": {
          "dataset.raw": "aoitrack-earthquake"
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
