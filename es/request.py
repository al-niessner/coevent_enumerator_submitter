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
    "query": { "match_all":{} },
    "filter": {
      "bool": {
        "must": [
          {
            "term": { "dataset_type.raw": "acquisition" }
          },
          {
            "term": { "dataset.raw": "acquisition-S1-IW_SLC" }
          },
          {
            "geo_shape": { "location": { "shape": {} } }
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

PAIR_ACQUISITION_WITH_ORBIT = '''
{
  "bool": {
    "must": [
      {
        "term": {
          "dataset.raw": "S1-AUX_POEORB"
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
}'''

def collate_acquisitions (begin, end, location):
    '''helper function to build request'''
    if not isinstance(begin,str): begin = begin.isoformat('T','seconds')+'Z'
    if not isinstance(end,str): end = end.isoformat('T','seconds')+'Z'

    request = json.loads (COLLATE_ACQUISITIONS)
    must = request['filtered']['filter']['bool']['must']
    must[-3]['geo_shape']['location']['shape'] = location
    must[-2]['range']['endtime']['gt'] = begin
    must[-1]['range']['starttime']['lt'] = end
    print (json.dumps(request))
    return request

def pair_acquisition_with_orbit (begin, end, resorb=False):
    '''helper function to build request'''
    if not isinstance(begin,str): begin = begin.isoformat('T','seconds')+'Z'
    if not isinstance(end,str): end = end.isoformat('T','seconds')+'Z'

    request = json.loads (PAIR_ACQUISITION_WITH_ORBIT)
    request['bool']['must'][-2]['range']['endtime']['gt'] = end
    request['bool']['must'][-1]['range']['starttime']['lt'] = begin

    if resorb:
        request['bool']['must'][0]['term']['dataset.raw'] = 'S1-AUX_RESORB'
        pass
    return request
