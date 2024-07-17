# South Africa Street History Mapping

We were curious about visualising how street names correlate to their language or place of origin in South Africa - a country whose history is marked by significant power struggles and complex race relations. This repo provides the code for creating maps of street networks colour coded by place of origin and language.

This readme is divided into:
* [Results](#results)
* [Academic Outputs](#academic-outputs)
* [Running the code](#running-the-code)
* [Helpful Notebooks](#running-the-code)
* [References](#references)

## Results

[//]: # (TODO: Fill in this section)
### Johannesburg

#### Soweto

#### Sandton

### Cape Town


## Academic Outputs
* [Poster for IC2S2 2024](https://drive.google.com/file/d/1oTQ1dDyFoRqsKCXKTvk2OtT13-hKzsPT/view?usp=drive_link)
* Paper coming soon!

## Running the code
This section describes how to run the code. Feel free to open an issue if you have any questions!

### Prerequisites

* If windows, git bash
* [Docker](https://docs.docker.com/desktop/)
* [Poetry](https://python-poetry.org/docs/)
* ~5GB Disk Space (Docker images + data)

### Setup
Poetry is used to manage packages and virtual environments.

```shell
 poetry shell
```

```shell
 poetry install
```

### Data Download Pipeline

#### 1. Retrieve streets for relevant countries
_Core Code:_ [download_country_streets.py](./src/street_list_download/download_country_streets.py)

We first need to download all street names for South Africa and selected countries that have played a role in South Africa's history (see [countries](src/utils/country_iso_map.py)). Data is downloaded using the [Overpass API](https://overpass-api.de) - an API that retrieves data easily from [OpenStreetMaps](https://www.openstreetmap.org/).

To retrieve street data, check that you're happy with what countries are being retrieved and run:
```shell
python ./src/street_list_download/main.py
```

If you're on a slurm enabled cluster, you can run
```shell
sbatch ./scripts/1_retrieve-streets.sbatch
```

The outputs of this script are saved to [streets](output/streets) in CSV format.

#### 2. Process street data
_Core Code:_ [preprocess_country_streets.py](./src/street_list_preprocessing/preprocess_country_streets.py)

We now process the street names for the various countries so that we end up with a dictionary of terms for the country. Each street name is:
* Exploded by space (e.g. so that Nottingham Road becomes [Nottingham, Road])
* Converted to lowercase

This results in a dataframe of terms. Empty, NaN, digit, and duplicate terms are dropped. Words less than a certain length are also dropped. 

To process the street data, run:
```shell
python ./src/street_list_preprocessing/main.py
```

If you're on a slurm enabled cluster, you can run
```shell
sbatch ./scripts/2_process-streets.sbatch
```

The outputs of this script are saved to [streets](output/streets) in CSV format with the prefix "processed". Additionally, all terms and the corresponding origin country are saved to a sqlite database in [output/street_history.sqlite](output/street_history.sqlite) in the table `street_terms`.

#### 3. Build Dictionary

_Core Code:_ [build_dictionary_for_term.py](./src/dictionary_builder/build_dictionary_for_term.py)

Now that we have all the terms for each selected country, we can build a lookup dictionary for each term for a "home" country. In our case, South Africa is the home country.

For each term in South Africa's terms data from the previous step, the term is looked up in the `street_terms` table. If the term is matched to one or more countries (including in the home country), the term is saved in a dictionary table and assigned a likelihood based on the frequency of the term appearing in different countries.

The term, origin, and likelihood are saved to a sqlite database in [output/street_history.sqlite](output/street_history.sqlite) in a table with the format `<country>_terms_dictionary`. 

To build a dictionary of terms for a specific country, run:
```shell
python ./src/dictionary_builder/main.py $COUNTRY
```

Where $COUNTRY is `south_africa` in the case of this repo but could be modified to other countries that have been downloaded.

If you're on a slurm enabled cluster, you can run:
```shell
sbatch ./scripts/3_build-dictionary-south-africa.sbatch
```

#### 4. Map
[//]: # (TODO: Fill in this section)


## Helpful Notebooks
[//]: # (TODO: Fill in this section)

- [Sandbox with geofabrik](notebooks/geofabrik-sandbox.ipynb) (requires pipeline to be run below)
- [Sandbox with osmnx](notebooks/osmnx-sandbox.ipynb)

## References
[//]: # (TODO: Fill in this section)
