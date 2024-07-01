import unittest
import pandas as pd
import numpy as np
from helper_lib import YearExtractor 

class TestYearExtractor(unittest.TestCase):
    """
    Unit tests for YearExtractor class to validate year extraction from various date formats.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the YearExtractor instance for testing.
        """
        cls.extractor = YearExtractor()

    def test_valid_date(self):
        """
        Test extracting year from a valid date in YYYY-MM-DD format.
        """
        self.assertEqual(self.extractor.extract_year('2020-06-01'), '2020')
    
    def test_valid_date_different_format(self):
        """
        Test extracting year from a valid date in YYYY/MM/DD format.
        """
        self.assertEqual(self.extractor.extract_year('2018/07/15'), '2018')
    
    def test_invalid_date(self):
        """
        Test handling of an invalid date format.
        """
        self.assertTrue(pd.isnull(self.extractor.extract_year('invalid-date')))
    
    def test_nan_value(self):
        """
        Test handling of NaN value.
        """
        self.assertTrue(pd.isnull(self.extractor.extract_year(np.nan)))
    
    def test_null_value(self):
        """
        Test handling of None value.
        """
        self.assertTrue(pd.isnull(self.extractor.extract_year(None)))
    
    def test_date_without_day(self):
        """
        Test extracting year from a date without a day component (YYYY-MM).
        """
        self.assertEqual(self.extractor.extract_year('2022-05'), '2022')
    
    def test_date_with_time(self):
        """
        Test extracting year from a date with time information (YYYY-MM-DD HH:MM:SS).
        """
        self.assertEqual(self.extractor.extract_year('2021-09-15 12:45:35'), '2021')

if __name__ == '__main__':
    unittest.main()