import sqlite3
import time

import pandas as pd
from mpi4py import MPI

from dictionary_builder.build_dictionary_for_term import build_dictionary_for_term, write_df_to_sql
from dictionary_builder.extract_country_from_args import extract_country
from dictionary_builder.initialise_terms_table import initialise_terms_table
from utils.env_variables import SQLITE_DB, MERGED_STREET_DATA_TABLE, MPI_TAGS
from utils.logger import get_logger

logger = get_logger()


def main(reset_db: bool = False) -> None:
    local_conn = sqlite3.connect(SQLITE_DB, timeout=10)

    start_time = time.time()
    comm = MPI.COMM_WORLD  # get MPI communicator object
    rank = comm.Get_rank()
    size = comm.Get_size()
    name = MPI.Get_processor_name()
    status = MPI.Status()   # get MPI status object

    country = extract_country()
    if country is None:
        return
    # Separate terms by country being processed

    country_terms = pd.read_sql_query(f"SELECT * FROM {MERGED_STREET_DATA_TABLE} WHERE country = ?", local_conn,
                                      params=[country])

    # Might want to setup some stuff here
    if rank == 0:
        logger.debug("I'm rank 0")
        logger.info(f"Building dictionary {country} with slurm")
        total_terms, number_unique_countries = initialise_terms_table(country, local_conn, reset_db)

        logger.info(
            f"Comparing {len(country_terms)} terms from {country} to {total_terms} terms from " +
            f"{number_unique_countries} countries (including {country})")

        num_workers = size - 1
        closed_workers = 0
        logger.info("Master starting with %d workers" % num_workers)
        while closed_workers < num_workers:
            source = status.Get_source()
            tag = status.Get_tag()
            results = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            logger.info(f"Got data from worker {source}, {tag}")
            print(results)
            if tag == MPI_TAGS.DONE:
                results = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
                logger.info(f"Got data from worker {source}")
                logger.info(results)
                # write_df_to_sql(country, results, local_conn)
            elif tag == MPI_TAGS.EXIT:
                logger.info(f"Worker {source} exited.")
                closed_workers += 1

    # Make sure rank 0 has done its stuff before moving on
    # MPI.COMM_WORLD.Barrier()

    else:
        # For each country
        with local_conn:
            for index, term in enumerate(country_terms["term"]):
                # If there are still files to process and processor is ready
                if index % size != rank:
                    continue

                logger.debug(
                    f"Item {term} is being done by processor {rank} ({name}) of {size}"
                )

                # Do stuff here!
                build_dictionary_for_term(country, term, local_conn, mpi_comm=comm)
            comm.send(None, dest=0, tag=MPI_TAGS.EXIT)
        # End do stuff

        # Finished
        logger.info(
            "Node %s time spent in minutes: %s",
            ((rank - 1) % size),
            int(time.time() - start_time) / 60,
        )


if __name__ == "__main__":
    main()
