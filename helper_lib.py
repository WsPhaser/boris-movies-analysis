import pandas as pd
import numpy as np

class YearExtractor:
    def extract_year(self, release_date):
        """
        Extracts the year from a release date string.

        This method attempts to convert the given release date to a datetime object and extract the year part.
        If the conversion fails or the input is null, it returns NaN.

        Parameters:
        release_date (str): A string representing the release date.

        Returns:
        str: The extracted year as a string if conversion is successful.
        np.nan: If the release date is null or conversion fails.
        """
        try:
            if pd.isnull(release_date):
                return np.nan
            return str(pd.to_datetime(release_date)).split('-')[0]
        except Exception as e:
            return np.nan
