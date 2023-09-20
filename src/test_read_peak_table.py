import unittest
from read_peak_table import read_mzmine3_peaktable

class TestReadPeakTable(unittest.TestCase):

    def test_read_peak_table(self):

        EXAMPLE_DATA_PATH = "./example_data"
        EXAMPLE_DATA_NAME = "example_peak_table.csv"

        df = read_mzmine3_peaktable(EXAMPLE_DATA_PATH, EXAMPLE_DATA_NAME)

        self.assertEqual(df.index.name, "id")