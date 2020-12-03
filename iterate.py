'''module that orchestrates all of the work
'''

import es
import es.request

def main():
    for response in es.query (es.request.all_active_aoi):
        aoi = response['_source']
        print (aoi)
        pass
    return

if __name__ == '__main__': main()
