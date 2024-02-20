import os
import time

from mpi4py import MPI

from street_list_download.download_country_streets import download_country_streets
from utils.country_iso_map import COUNTRY_ISO_MAP
from utils.env_variables import STREET_DATA_DIR
from utils.logger import get_logger

logger = get_logger()


def retrieve_street_list() -> None:
    logger.info("Retrieving street list for countries with slurm")

    start_time = time.time()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    name = MPI.Get_processor_name()

    # Might want to setup some stuff here
    if rank == 0:
        logger.debug("I'm rank 0")
        if not os.path.exists(STREET_DATA_DIR):
            os.makedirs(STREET_DATA_DIR)

    # Make sure rank 0 has done its stuff before moving on
    MPI.COMM_WORLD.Barrier()

    # Get a list of countries
    countries = COUNTRY_ISO_MAP.keys()

    # For each country
    for index, country in enumerate(countries):
        # If there are still files to process and processor is ready
        if index % size != rank:
            continue

        logger.info(
            f"Item {country} is being done by processor {rank} ({name}) of {size}"
        )

        # Do stuff here!
        download_country_streets(country)

    # End do stuff

    # Finished
    logger.info(
        "Node %s time spent in minutes: %s",
        ((rank - 1) % size),
        int(time.time() - start_time) / 60,
    )


def main() -> None:
    retrieve_street_list()


if __name__ == "__main__":
    main()
