# South Africa Street History Mapping
A small repo to generate a map of South Africa's streets colour coded by the name's origin.

## Prerequisites
* If windows, git bash
* Docker
* Poetry

## Pipeline

#### 1. List Open Street Maps Locations
To get a list of all available locations downloadable via geofabrik, run:
```shell
./scripts/geofabrik-list-locations.sh
```

From the output, you can identify which regions you want to download for the following step.

### 2. Download open street map data for region
Use the [`geofabrik-download-locations`](./scripts/geofabrik-download-locations.sh) to download the Open Street Map data for your selected location.

Here is the script for south africa:
```shell
./scripts/geofabrik-download-locations.sh africa/south-africa
```