import sqlite3
import time

import pandas as pd
from mpi4py import MPI

from dictionary_builder.build_dictionary_for_term import build_dictionary_for_term
from dictionary_builder.extract_country_from_args import extract_country
from dictionary_builder.initialise_terms_table import initialise_terms_table
from utils.env_variables import SQLITE_DB, MERGED_STREET_DATA_TABLE
from utils.logger import get_logger

logger = get_logger()

conn = sqlite3.connect(SQLITE_DB, timeout=10)


def main(reset_db: bool = False) -> None:

    start_time = time.time()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    name = MPI.Get_processor_name()

    country = extract_country()
    if country is None:
        return
    # Separate terms by country being processed

    country_terms = pd.read_sql_query(f"SELECT * FROM {MERGED_STREET_DATA_TABLE} WHERE country = ?", conn,
                                      params=[country])

    # Might want to setup some stuff here
    if rank == 0:
        logger.debug("I'm rank 0")
        logger.info(f"Building dictionary {country} with slurm")
        total_terms, number_unique_countries = initialise_terms_table(country, conn, reset_db)

        logger.info(
            f"Comparing {len(country_terms)} terms from {country} to {total_terms} terms from " +
            f"{number_unique_countries} countries (including {country})")

    # Make sure rank 0 has done its stuff before moving on
    MPI.COMM_WORLD.Barrier()

    # For each country
    for index, term in enumerate(country_terms["term"]):
        # If there are still files to process and processor is ready
        if index % size != rank:
            continue

        logger.debug(
            f"Item {term} is being done by processor {rank} ({name}) of {size}"
        )

        # Do stuff here!
        build_dictionary_for_term(country, term, conn)

    # End do stuff

    # Finished
    logger.debug(
        "Node %s time spent in minutes: %s",
        ((rank - 1) % size),
        int(time.time() - start_time) / 60,
    )


if __name__ == "__main__":
    with conn:
        main()
