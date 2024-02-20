import sqlite3
import time

from mpi4py import MPI

from street_list_preprocessing.get_country_street_files import get_country_street_files
from street_list_preprocessing.preprocess_country_streets import preprocess_country_streets
from utils.env_variables import SQLITE_DB, MERGED_STREET_DATA_TABLE
from utils.logger import get_logger

logger = get_logger()

conn = sqlite3.connect(SQLITE_DB)


def preprocess_streets() -> None:
    logger.info("Preprocess street list for countries")

    start_time = time.time()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    name = MPI.Get_processor_name()

    # Might want to setup some stuff here
    if rank == 0:
        logger.debug("I'm rank 0")

    # Make sure rank 0 has done its stuff before moving on
    MPI.COMM_WORLD.Barrier()

    # Remove previous results
    conn.execute(f"DROP TABLE IF EXISTS {MERGED_STREET_DATA_TABLE}")

    # Get a list of country street files
    countries = get_country_street_files()

    # For each file
    for index, country_file in enumerate(countries):

        # If there are still files to process and processor is ready
        if index % size != rank:
            continue

        logger.info(
            f"Item {country_file} is being done by processor {rank} ({name}) of {size}"
        )

        # Do stuff here!
        preprocess_country_streets(country_file)

    # End do stuff

    # Finished
    logger.info(
        "Node %s time spent in minutes: %s",
        ((rank - 1) % size),
        int(time.time() - start_time) / 60,
    )


def main() -> None:
    with conn:
        preprocess_streets()


if __name__ == "__main__":
    main()
