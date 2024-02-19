import os.path
import sys
from pathlib import Path

import pandas as pd
from thefuzz import process

from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP
from utils.env_variables import MERGED_STREET_DATA_FILE, FUZZY_MATCH_THRESHOLD, TERMS_DICTIONARY
from utils.logger import get_logger

logger = get_logger()


def build_dictionary(country: str) -> None:
    logger.info(f"Building dictionary of street origins for country {country}")
    terms_df = pd.read_csv(MERGED_STREET_DATA_FILE)

    # Separate terms by country being processed
    country_terms = terms_df[terms_df["country"] == country]
    terms_df = terms_df[terms_df["country"] != country]
    countries_df = terms_df["country"]
    number_unique_countries = len(terms_df["country"].unique())
    logger.info(f"Comparing terms from {country} to {number_unique_countries} other countries")

    threshold = FUZZY_MATCH_THRESHOLD

    output = []
    for term in country_terms["name"]:

        exact_match = terms_df[terms_df["name"] == term]
        # TODO: Favour exact match over fuzzy
        print(exact_match)

        matches = process.extractBests(term, terms_df["name"], limit=number_unique_countries, score_cutoff=threshold)
        print(matches)
        highest_probability = matches[0][1]
        for match in matches:
            probability = match[1]

            if probability < highest_probability:
                break

            index = matches[0][2]
            matching_country = countries_df[index]
            result = {
                "term": term,
                "origin": matching_country,
                "probability": probability
            }
            output.append(result)
        break

    output_df = pd.DataFrame(output)
    # Write result to csv
    output_file = Path(os.path.join("output", f"{country}_{TERMS_DICTIONARY}"))
    output_df.to_csv(output_file, index=False)

    output_df.to_csv()


def main() -> None:
    if len(sys.argv) < 2:
        logger.error("Please provide a country")
        return

    country = sys.argv[1]
    possible_countries = COUNTRY_ISO_CODE_NAME_MAP.values()

    if country in possible_countries:
        build_dictionary(country)
    else:
        output = ""
        for x in sorted(possible_countries):
            output = f"{output}- {x}\n"

        logger.error(f"Unknown country. Possible values are:\n{output}")
        return


if __name__ == "__main__":
    main()
