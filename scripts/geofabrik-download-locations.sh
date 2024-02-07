LOCATION=$1
data_dir="/${PWD}/data/tileset"

 docker run -it --rm -u $(id -u ${USER}):$(id -g ${USER}) \
           -v "${data_dir}:/tileset" \
           openmaptiles/openmaptiles-tools \
           download-osm geofabrik --state state.txt ${LOCATION}
