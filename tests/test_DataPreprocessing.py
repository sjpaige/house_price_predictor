from unittest import TestCase
import DataPreprocessing
from matplotlib.figure import Figure

class Test_DataPreprocessing(TestCase):
    """
    Run tests on the data preprocessing functions.
    """

    # Test if the create plots function correctly executes and produces a Figure
    def test_create_plots(self):
        self.assertTrue(isinstance(DataPreprocessing.create_plots(), Figure))





