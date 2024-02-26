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

The following pipelines are used to generate results.

## Data Download Pipeine

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

#### Countries

**Repeat this step for the following countries:**

| Code                                  | OSM Size [GB] |
|---------------------------------------|---------------|
| `africa/south-africa`                 | 0.3           |
| `europe/belgium`                      | 0.6           |
| `europe/france`                       | 4.2           |
| `europe/germany`                      | 4.0           |
| `europe/ireland-and-northern-ireland` | 0.3           |
| `europe/italy`                        | 1.8           |
| `europe/netherlands`                  | 1.2           |
| `europe/portugal`                     | 0.3           |
| `europe/spain`                        | 1.1           |
| `europe/great-britain/england`        | 1.3           |
| `europe/great-britain/scotland`       | 0.3           |
| `europe/great-britain/wales`          | 0.1           |
|                                       |               |
| **Total**                             | ~16GB         |

#### Manual Download

If any partigular locations do not download or you need to avoid docker, you can manually download the data
from [Geofabrik](https://download.geofabrik.de/) - e.g. for Germany:

```bash
# Linux
wget https://download.geofabrik.de/europe/germany-latest.osm.pbf -O ./data/europe/germany

# Windows
curl https://download.geofabrik.de/europe/germany-latest.osm.pbf -o ./data/europe/germany
```

### 4. [*Optional!*] Convert osm data to sqlite

SQLite is somewhat easier to work with and query but not entirely necessary. If you plan to do additional work on the
data beyond what is provided in the source code of this repo, you may want to complete this step.

For reference, this is the expected extracted sizes for the countries above:

| Code                                  | OSM Size [GB] | SQLite Size [GB] |
|---------------------------------------|---------------|------------------|
| `africa/south-africa`                 | 0.3           | 2.1              |
| `europe/belgium`                      | 0.6           | 3.6              |
| `europe/france`                       | 4.2           | 24.6             |
| `europe/germany`                      | 4.0           | 25.2             |
| `europe/ireland-and-northern-ireland` | 0.3           | 2.5              |
| `europe/italy`                        | 1.8           | 11.2             |
| `europe/netherlands`                  | 1.2           | 8.3              |
| `europe/portugal`                     | 0.3           | 2.0              |
| `europe/spain`                        | 1.1           | 7.1              |
| `europe/great-britain/england`        | 1.3           | 8.0              |
| `europe/great-britain/scotland`       | 0.3           | 1.5              |
| `europe/great-britain/wales`          | 0.1           | 0.7              |
|                                       |               |                  |
| **Total**                             | ~16GB         | ~98GB            |

Use the [`gdal convert script`](./scripts/gdal-convert-osm-to-sql.sh) to convert the OSM data to sqlite (an easier
format to work with in python).

```shell
./scripts/gdal-convert-osm-to-sql.sh africa/south-africa
```

Repeat for all downloaded countries.

You should now have a `.sqlite` file in the [data directory](data) for your selected locations.

#### Manual Conversion

Under the hood, this script uses a docker container with `gdal` installed (
see [docs](https://github.com/OSGeo/gdal/tree/master/docker)). Version 3.6.4 of `gdal` is used because, at the time of
writing, it successfully converts osm to sqlite without RAM issues.

If you want to avoid docker, you can ensure you have [`gdal` installed](https://gdal.org/download.html) on your system
and run the command passed into the
docker container:

```shell
# Replace LOCATION with the region directory you want to work in
# e.g. africa/south-africa
cd data/${LOCATION}

# Replace filename below with relevant filename in LOCATION
# e.g. south-africa-latest
ogr2ogr -overwrite -f SQLite -lco FORMAT=WKT "${filename}.sqlite" "${filename}.osm.pbf"
```

### 5. [*Optional!*] Move data to remote server

You'll need `rsync` for this step.
You can run the following from the root project directory to sync the data across to
a remote server if need be:

```shell
rsync -avm --include='*/' --include='*.osm.pbf' --exclude='*' ./data ${REMOTE}:${REMOTE_DIRECTORY}
```

## Dictionary Generation

[//]: # (TODO: Document this some more)

#### 1. List Open Street Maps Locations

## Relevant Notebooks

- [Sandbox with geofabrik](notebooks/geofabrik-sandbox.ipynb) (requires pipeline to be run below)
- [Sandbox with osmnx](notebooks/osmnx-sandbox.ipynb)
