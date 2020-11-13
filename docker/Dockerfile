FROM hysds/pge-base:develop-es1

MAINTAINER aria-ops "jlinick@.jpl.nasa.gov"
LABEL description="AOI Enumerator Submitter Container"

# copy packages
COPY . /home/ops/verdi/ops/aoi_enumerator_submitter
RUN set -ex \
 && source /home/ops/verdi/bin/activate \
 && sudo chown -R ops:ops /home/ops/verdi/ops/aoi_enumerator_submitter \
 && cd /home/ops/verdi/ops/aoi_enumerator_submitter  \
 && pip install numpy

# set entrypoint
USER ops
WORKDIR /home/ops
CMD ["/bin/bash", "--login"]
