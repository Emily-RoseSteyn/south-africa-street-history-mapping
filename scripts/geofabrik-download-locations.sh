LOCATION=$1
DATA_DIR="/${PWD}/data/tileset"

 docker run -it --rm -u $(id -u ${USER}):$(id -g ${USER}) \
           -v "${DATA_DIR}:/tileset" \
           openmaptiles/openmaptiles-tools \
           download-osm geofabrik --state state.txt ${LOCATION}
