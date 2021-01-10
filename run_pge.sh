#! /usr/bin/env bash

# source environment
source $HOME/verdi/bin/activate

# source ISCE env
source /opt/isce2/isce_env.sh

# do the actual PGE work
/home/ops/verdi/ops/coseismic_enumerator/iterate.py

# the sleep is to keep the container around for debugging purposes
sleep 600
