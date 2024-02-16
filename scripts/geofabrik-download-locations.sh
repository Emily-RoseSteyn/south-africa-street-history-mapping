LOCATION=${1:?"Error. You must supply a location."}
# Assuming running from project root
working_dir="data/${LOCATION}"
data_dir="/${PWD}/${working_dir}"

docker run -it --rm \
  -v "${data_dir}:/tileset" \
  openmaptiles/openmaptiles-tools \
  download-osm geofabrik --state state.txt ${LOCATION}
