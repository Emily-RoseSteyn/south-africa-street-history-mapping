LOCATION=${1:?"Error. You must supply a location."}
# Assuming running from project root
working_dir="data/${LOCATION}"
data_dir="/${PWD}/${working_dir}"

number_finds=$(find ${working_dir} -type f -name \*.osm.pbf | wc -l)

if (( ${number_finds} > 1 )); then
  echo '%s\n' "Error! More than one osm file found in location ${LOCATION}" >&2
  exit 1
fi

pbf_filepath=$(find ${working_dir} -type f -name \*.osm.pbf)
filename_full=$(basename -- ${pbf_filepath})
filename="${filename_full%%.*}"

echo ${pbf_filepath}
echo ${filename_full}
echo ${filename}

docker run -it --rm \
        -v "${data_dir}:/data" \
        -w "//data" \
        ghcr.io/osgeo/gdal:ubuntu-full-3.6.4 \
        ogr2ogr -overwrite -f SQLite -lco FORMAT=WKT "${filename}.sqlite" "${filename_full}"

# Note:
# At the time of writing, specifically needed version 3.6.4 for no errors or ram issues to happen when executing ogr2ogr
# Double slash on working directory used because of windows issue with working directory - potentially remove if on linux?