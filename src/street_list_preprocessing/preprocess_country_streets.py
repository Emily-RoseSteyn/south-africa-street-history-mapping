import os
import sqlite3
from pathlib import Path

import pandas as pd

from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP
from utils.env_variables import PROCESSED_STREET_DATA_DIR, WORD_LENGTH_THRESHOLD, SQLITE_DB, MERGED_STREET_DATA_TABLE
from utils.logger import get_logger

logger = get_logger()

conn = sqlite3.connect(SQLITE_DB)


def write_dataframe_to_csv(df: pd.DataFrame, file_name: str):
    output_dir = PROCESSED_STREET_DATA_DIR

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, file_name)
    df.to_csv(output_file, index=False)


def write_to_sql(df: pd.DataFrame):
    df.to_sql(MERGED_STREET_DATA_TABLE, conn, if_exists='append', index=False)


def preprocess_country_streets(country_file):
    logger.info(
        f"File {country_file} is being processed"
    )
    # Determine iso code
    file_name = os.path.basename(country_file)
    country = Path(file_name).stem
    country_code_map = COUNTRY_ISO_CODE_NAME_MAP
    iso_code = list(country_code_map.keys())[list(country_code_map.values()).index(country)]

    # Load CSV
    df = pd.read_csv(country_file)
    logger.info(
        f"Found {len(df)} streets"
    )

    # Explode words
    df['name'] = df['name'].str.split(r'\W')
    df = df.explode('name', ignore_index=True)

    # Lowercase
    df = df.apply(lambda x: x.astype(str).str.lower())

    # Aggregate (with frequency)
    df = df.groupby(['name']).size().reset_index(name='frequency')
    df = df.sort_values(by=['frequency'], ascending=False)

    # Write intermediate file to csv
    write_dataframe_to_csv(df, f"intermediate_{file_name}")

    prefiltered_total = len(df)
    logger.info(
        f"Found a total of {prefiltered_total} terms"
    )

    # Filter nans, empty, digits etc
    df["name"] = df["name"].str.extract(r'(\D+)')
    df = df.dropna()

    # Remove duplicates once more at this stage
    df = df.groupby(['name']).agg({'frequency': 'max'}).reset_index()

    # Dropped words
    dropped_df = df[df['name'].str.len() < WORD_LENGTH_THRESHOLD]
    write_dataframe_to_csv(dropped_df, f"dropped_words_{file_name}")

    # Ignore words that are less than word length threshold
    df = df[df['name'].str.len() >= WORD_LENGTH_THRESHOLD]

    total = len(df)
    dropped = prefiltered_total - total
    logger.info(
        f"Dropped {dropped} terms"
    )
    logger.info(
        f"{total} terms remaining"
    )

    # TODO: Figure out which words to remove completely (custom stop words)
    # TODO: Remove stop words

    # Add country and iso_code
    df['country'] = country
    df['iso_code'] = iso_code

    # Save dataframe of specific street terms - term, frequency, country, country_iso_code
    df = df.rename(columns={"name": "term"})
    write_dataframe_to_csv(df, f"processed_{file_name}")

    # Write to merged SQL table
    write_to_sql(df)

    logger.info('\n')
