from unittest import TestCase
import KmeansAnalysis
from matplotlib.figure import Figure

class Test(TestCase):

    def test_get_clustering_plot(self):
        """ Test all the perms of the cluster plot to make sure they return the proper type
            all dependent values are also tested"""
        self.assertIsNotNone(KmeansAnalysis.home_data)
        self.assertIsNotNone(KmeansAnalysis.scaled_data)
        self.assertIsNotNone(KmeansAnalysis.price_data)
        self.assertTrue(isinstance(KmeansAnalysis.get_clustering_plot('price'), Figure))
        self.assertTrue(isinstance(KmeansAnalysis.get_clustering_plot('clusters'), Figure))