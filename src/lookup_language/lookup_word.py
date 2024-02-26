import pandas as pd
from lingua import Language, LanguageDetectorBuilder


class LanguageDetector:
    def __init__(self):
        self._languages = [
            Language.AFRIKAANS,
            Language.DUTCH,
            Language.ENGLISH,
            Language.FRENCH,
            Language.GERMAN,
            Language.ITALIAN,
            Language.PORTUGUESE,
            Language.SOTHO,
            Language.SPANISH,
            Language.XHOSA,
            Language.ZULU,
        ]
        self._detector = LanguageDetectorBuilder.from_languages(*self._languages).build()

    def detect(self, term):
        confidence_values = self._detector.compute_language_confidence_values(term)
        modified_result = []
        for result in confidence_values:
            modified_result.append((term, result.language.name, result.value))
        df_confidence_values = pd.DataFrame(modified_result, columns=['term', 'language', 'likelihood'])
        df_confidence_values["language"] = df_confidence_values["language"].apply(lambda x: x.lower())
        df_confidence_values["likelihood"] = df_confidence_values["likelihood"] * 100
        return df_confidence_values
