working_dir="data"
data_dir="/${PWD}/${working_dir}"

pbf_filepath=$(find . -type f -name \*.osm.pbf)
filename=$(basename -- ${pbf_filepath})
filename="${filename%%.*}"

docker run -it --rm \
        -v "${data_dir}:/data" \
        ghcr.io/osgeo/gdal:ubuntu-full-latest \
        ogr2ogr --debug ON -overwrite -f SQLite -lco FORMAT=WKT "${working_dir}/${filename}.sqlite" ${pbf_filepath}

#TODO: Convert here is too big for RAM