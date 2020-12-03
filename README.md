# Co-Event Enumerator Submitter

Iterates through orbit an determining the relevant co-event AOIs overlaps, then submits enumeration jobs for the matching tracks and AOI.

# Running

1. Obtain orbit start and stop times
2. Loop through active coseismic AOIs (end date further out than todays date)
    1. Find all acquisitions within orbit start/end time and within AOI
    2. Submit job(s) to enumerator

