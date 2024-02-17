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

## Relevant Notebooks

- [Sandbox with geofabrik](notebooks/geofabrik-sandbox.ipynb) (requires pipeline to be run below)
- [Sandbox with osmnx](notebooks/osmnx-sandbox.ipynb)

## Pipeline for Dictionary Generation

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

**Repeat this step for the following countries:**

| Code                                  | Size [GB] |
|---------------------------------------|-----------|
| `africa/south-africa`                 | 0.3       |
| `europe/belgium`                      | 0.6       |
| `europe/france`                       | 4.2       |
| `europe/germany`                      | 4.0       |
| `europe/ireland-and-northern-ireland` | 0.3       |
| `europe/italy`                        | 1.8       |
| `europe/netherlands`                  | 1.2       |
| `europe/portugal`                     | 0.3       |
| `europe/spain`                        | 1.1       |
| `europe/great-britain/england`        | 1.3       |
| `europe/great-britain/scotland`       | 0.3       |
| `europe/great-britain/wales`          | 0.1       |
|                                       |           |
| **Total**                             | ~16GB     |

### 4. Convert osm data to sqlite

Use the [`gdal convert script`](./scripts/gdal-convert-osm-to-sql.sh) to convert the OSM data to sqlite (an easier
format to work with in python).

```shell
./scripts/gdal-convert-osm-to-sql.sh africa/south-africa
```

Repeat for all downloaded countries.

You should now have a `.sqlite` file in the [data directory](data) for your selected locations.

