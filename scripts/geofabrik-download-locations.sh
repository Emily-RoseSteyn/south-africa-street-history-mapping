LOCATION=$1
# Assuming running from project root
data_dir="data/${LOCATION}"

mkdir -p ${data_dir}

docker run -it --rm -u $(id -u ${USER}):$(id -g ${USER}) \
  -v "/${PWD}/${data_dir}:/tileset" \
  openmaptiles/openmaptiles-tools \
  download-osm geofabrik --state state.txt ${LOCATION}
