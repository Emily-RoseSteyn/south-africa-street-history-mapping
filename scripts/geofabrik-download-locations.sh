LOCATION=$1
# Assuming running from project root
data_dir="data/${LOCATION}"

docker run -it --rm \
  -v "/${PWD}/${data_dir}:/tileset" \
  openmaptiles/openmaptiles-tools \
  download-osm geofabrik --state state.txt ${LOCATION}
