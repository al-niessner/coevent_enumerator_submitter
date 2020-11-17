# Co-Event Enumerator Submitter

Iterates through orbit an determining the relevant co-event AOIs overlaps, then submits enumeration jobs for the matching tracks and AOI.

# Running

1. Extract tracks from the input
1. Use elastic search to find all active co-event AOIs
1. Reduce the AOIs to just those containing any of the input tracks -- can ES do this?
1. Submit enumerator for any/all tracks with matching AOIs
