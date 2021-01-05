from unittest import TestCase
import RegressionPrediction
from matplotlib.figure import Figure

class TestPredictionTrainer(TestCase):

    def test_predict_house_price(self):
        """ Test to make sure that the prediction engine can produce a prediction that is on target"""
        regressor = RegressionPrediction.PredictionTrainer()
        test_fields = [1, 1, 1000, 1, 1, 1, 1, 0, 1900, 0, 44, 77]
        target = 371343.5
        self.assertEqual(regressor.predict_house_price(test_fields), target)

    def test_get_reg_pred_prices(self):
        """ Test to make sure that the plot of the regression line is the correct type and returns"""
        regressor = RegressionPrediction.PredictionTrainer()
        self.assertTrue(isinstance(regressor.get_reg_pred_prices(), Figure))
