import sqlite3

import pandas as pd
from tqdm import tqdm

from lookup_language.lookup_word import LanguageDetector
from utils.env_variables import SQLITE_DB, TERMS_DICTIONARY_TABLE, TERMS_LANGUAGE_DICTIONARY_TABLE
from utils.logger import get_logger

logger = get_logger()

conn = sqlite3.connect(SQLITE_DB)


def _write_df_to_sql(df: pd.DataFrame) -> None:
    if df is None:
        return
    df.to_sql(
        TERMS_LANGUAGE_DICTIONARY_TABLE,
        conn,
        if_exists='append',
        index=False)


def main() -> None:
    logger.info(f"Looking up language of South African terms")
    language_detector = LanguageDetector()
    terms = pd.read_sql(f"SELECT term FROM south_africa_{TERMS_DICTIONARY_TABLE} where country = ?", conn,
                        params=["south_africa"])

    for term in tqdm(terms["term"]):
        result = language_detector.detect(term)
        _write_df_to_sql(result)


if __name__ == "__main__":
    main()
