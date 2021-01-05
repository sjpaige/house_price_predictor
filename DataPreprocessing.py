"""
Data Preprocessing handles processing and analyzing the raw housing data and making it
usable for KMeansAnalysis and RegressionPrediction modules, as well as generating some
figures that describe how/why the data was filtered the way it was.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import DatabaseConnection as dc
from matplotlib.figure import Figure

# Open the database connection
conn = dc.connect()
# Download the data from the database
house_data_raw = dc.download_raw_housing_data(conn)
# Drop null data
house_data_raw.dropna()

def create_plots():
    """
    Creates a h-bar plot of the correlation values of all the features with the price sorted in descending order.

    Creates an outliers plot of the price showing the distribution across the dataset.

    :return: a Figure object that holds the information about two subplots
    """

    figure = Figure(figsize=(5,8))
    sub_fig_corr = figure.add_subplot(211)
    house_data_raw.corr()['price'].sort_values().plot(kind='barh', ax=sub_fig_corr)
    sub_fig_corr.set(title='Price Correlation Chart')

    sub_fig_outliers = figure.add_subplot(212)
    price_data = house_data_raw['price']
    sns.kdeplot(data=price_data, shade=True, ax=sub_fig_outliers)
    sub_fig_outliers.set(xlabel='Price (millions)', ylabel='Density Value', title='Price Distribution')
    plt.tight_layout()
    return figure

def upload_to_db_post_processed_data():
    """
    Calls the database upload command after the features are filtered then the DataFrame is
    uploaded to the database.

    Chosen features: price, bedrooms, bathrooms, sqft_living, floors, waterfront, view, grade,
    sqft_basement, yr_built, yr_renovated, lat, long

    Not chosen: id, date, sqft_lot, condition, sqft_above, zipcode, sqft_living15, sqft_lot15
    These were not chose because they either have low correlation with the price or they are
    redundant to another feature.
    """
    house_features = ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'floors',
                      'waterfront', 'view', 'grade', 'sqft_basement', 'yr_built', 'yr_renovated', 'lat', 'long']
    house_data = house_data_raw[house_features]
    dc.upload_processed_data(house_data, conn)
