 docker run -it --rm -u $(id -u ${USER}):$(id -g ${USER}) \
           openmaptiles/openmaptiles-tools \
           download-osm list geofabrik