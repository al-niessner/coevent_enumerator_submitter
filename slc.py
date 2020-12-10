'''encapsulate all that it takes to get an SLC localized'''

def load (acquisition):
    '''load SLC from DAACs if it is not already here

    This is going to send jobs to a Localizer queue.
    '''
    #
    # FIXME: need more here to start the localization process
    #
    return acquisition['_id'].split('-')[1]
