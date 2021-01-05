"""
RegressionPrediction handles the prediction of house prices from the processed data in the database.

It also creates a reg plot of this data for display by the UI.
"""
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import seaborn as sns
import DatabaseConnection as dc
import pandas as pd

class PredictionTrainer:
    """
    Class that combines the entire prediction process into a single entity
    """
    def __init__(self):
        # Get the data from the database
        conn = dc.connect()
        housing_data = dc.download_housing_data(conn)
        conn.close()

        price_data = housing_data['price'] # Choose the price data as the target
        housing_data.drop(['price'], axis=1, inplace=True) # Drop the price data from the main feature set
        # Split the dataset into a traning set and test set.
        self.X = housing_data
        self.y = price_data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.10, random_state=102)

        # Train the data with Linear Regression.
        # Outcome has a lower accuracy of mean absolute error: 127497.25764150245 r2 score: 0.6914914635024427
        # Instead a RandomForestRegressor should be used for higher accuracy prediction value
        # regressor = LinearRegression()
        # regressor.fit(X_train, y_train)
        # y_predict = regressor.predict(X_test)

        # Use a RandomForestRegressor() to create a prediction
        self.regressor = RandomForestRegressor(random_state=102)
        self.regressor.fit(self.X_train, self.y_train)
        self.y_predict = self.regressor.predict(self.X_test)

        # # Check the accuracy of the prediction with the mean absolute error and the r2 scores
        self.maerr = mean_absolute_error(self.y_test, self.y_predict)
        self.r2 = r2_score(self.y_test, self.y_predict)

    def predict_house_price(self,fields_data):
        """
        Takes in the features from the fields and returns a predicted value for the house.
        :return: predicted value for house
        """
        house_features = pd.DataFrame(
            [fields_data], columns=['bedrooms', 'bathrooms', 'sqft_living', 'floors',
                      'waterfront', 'view', 'grade', 'sqft_basement', 'yr_built', 'yr_renovated', 'lat', 'long'])


        return self.regressor.predict(house_features)[0]

    def get_reg_pred_prices(self):
        """
        Creates and returns a seaborn regplot of the predicted house prices vs the actual house prices.
        :return: a Figure object
        """
        reg_plot_price = sns.regplot(x=self.y_test, y=self.y_predict).get_figure()
        plt.xlabel('True Values [Price]')
        plt.ylabel('Predictions [Price]')
        plt.title('RandomForest Regression predictions for the test data')
        return reg_plot_price