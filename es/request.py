'''module to hold the Elastic-Search query objects

Rather than pollute the code with the query information, hide them behind
a variable name.
'''

import datetime
import json

ALL_ACTIVE_AOI = json.loads('''
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
            "gt": "''' + datetime.datetime.utcnow().isoformat('T','seconds') +
                            '''Z"
          }
        }
      }
    ]
  }
}''')


COLLATE_ACQUISITIONS = '''
{
  "filtered": {
    "query": {
      "geo_shape": {
        "location": {
          "shape": ""
        }
      }
    }
    "filter":{
      "bool": {
        "must": [
          {
            "term": {
              "dataset_type.raw": "acquisition"
            }
          },
          {
            "term": {
              "dataset.raw": "acquisition-S1-IW_SLC"
            }
          },
          {
            "range": {
              "endtime": {
                "gt": ""
              }
           }
         },
         {
            "range": {
              "starttime": {
                "lt": ""
              }
            }
         }
       ]
     }
   }
 }
}'''

def collate_acquisitions (begin, end, location):
    '''helper function to build request'''
    if not isinstance(begin,str): begin = begin.isoformat('T','seconds')+'Z'
    if not isinstance(end,str): end = end.isoformat('T','seconds')+'Z'

    request = json.loads (COLLATE_ACQUISITIONS)
    must = request['filtered']['filter']['bool']['must']
    must[-2]['range']['endtime']['gt'] = begin
    must[-1]['range']['starttime']['lt'] = end
    query = request['filtered']['query']
    query['geo_shape']['location']['shape'] = location
    return request
