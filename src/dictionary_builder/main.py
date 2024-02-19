import os.path
import sys
from pathlib import Path

import pandas as pd
from tqdm import tqdm

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

    output_df = pd.DataFrame(columns=["name", "country", "iso_code", "likelihood"])
    # Favour exact match over fuzzy
    for term in tqdm(country_terms["name"]):
        # TODO: If term not found
        # Any ways to speed up processing?
        exact_match = terms_df[terms_df["name"] == term]

        if len(exact_match) == 1:
            exact_match.assign(likelihood=[100])

        # If more than one exact match, work out countries to retain
        if len(exact_match) > 1:
            likelihoods = exact_match["frequency"] * 100 / exact_match["frequency"].sum()
            exact_match.insert(column="likelihood", value=likelihoods, loc=len(exact_match.columns))
            exact_match = exact_match.sort_values(by=["likelihood"], ascending=False).reset_index(drop=True)
            threshold_index = exact_match['likelihood'].cumsum().gt(threshold).idxmin() + 1
            exact_match = exact_match.loc[:threshold_index]

        output_df = pd.concat([output_df, exact_match], ignore_index=True)
        #
        # matches = process.extractBests(term, terms_df["name"], limit=number_unique_countries, score_cutoff=threshold)
        # print(matches)
        # highest_probability = matches[0][1]
        # for match in matches:
        #     probability = match[1]
        #
        #     if probability < highest_probability:
        #         break
        #
        #     index = matches[0][2]
        #     matching_country = countries_df[index]
        #     result = {
        #         "term": term,
        #         "origin": matching_country,
        #         "probability": probability
        #     }
        #     output.append(result)

    output_df = output_df.rename({"name": "term"}).drop(['frequency'], axis=1)

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
