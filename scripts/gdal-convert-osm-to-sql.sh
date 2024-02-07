working_dir="data"
data_dir="/${PWD}/${working_dir}"

pbf_filepath=$(find . -type f -name \*.osm.pbf)
filename=$(basename -- ${pbf_filepath})
filename="${filename%%.*}"

docker run -it --rm -u $(id -u ${USER}):$(id -g ${USER}) \
        -v "${data_dir}:/data" \
        ghcr.io/osgeo/gdal:ubuntu-full-latest \
        ogr2ogr -f SQLite -lco FORMAT=WKT "${working_dir}/${filename}.sqlite" ${pbf_filepath}

