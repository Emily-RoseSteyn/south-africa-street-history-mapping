# South Africa Street History Mapping

A small repo to generate a map of South Africa's streets colour coded by the name's origin.

## Prerequisites

* If windows, git bash
* [Docker](https://docs.docker.com/desktop/)
* [Poetry](https://python-poetry.org/docs/)
* ~5GB Disk Space (Docker images + data)

## Setup

```shell
 poetry shell
```

```shell
 poetry install
```
## Pipeline


## Deprecated Pipeline
**Note**: Ran into issues with this approach because the conversion from osm to sqlite does not complete successfully because of hitting max ram. Chose to instead rely on osmx as above.

#### 1. List Open Street Maps Locations

To get a list of all available locations downloadable via geofabrik, run:

```shell
./scripts/geofabrik-list-locations.sh
```

From the output, you can identify which regions you want to download for the following step.

### 2. Download open street map data for region

Use the [`download locations script`](./scripts/geofabrik-download-locations.sh) to download the Open Street Map data
for your selected location.

Here is the script for south africa:

```shell
./scripts/geofabrik-download-locations.sh africa/south-africa
```

### 3. Convert osm data to sqlite

Use the [`gdal convert script`](./scripts/gdal-convert-osm-to-sql.sh) to convert the OSM data to sqlite (an easier
format to work with in python).

```shell
./scripts/gdal-convert-osm-to-sql.sh
```

You should now have a `.sqlite` file in the [data directory](data) for your selected location.

