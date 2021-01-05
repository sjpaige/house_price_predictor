"""
A module that handles communication with the database.

Upload and download data from the database.
Get a connection object to the database.
Handle users in the database.
"""
import sqlite3
from sqlite3 import Error
import pandas as pd
import os

# The path to the database
current_directory = os.path.dirname(os.path.abspath(__file__))
database_location = os.path.join(current_directory, "mccore_investing_database.db")


def connect():
    """
    Opens a new connection to the sqlite3 database
    :return: a sqlite3.Connection object
    """
    connection = None
    try:
        connection = sqlite3.connect(database_location)
    except Error as err:
        print(err)

    return connection


# Select all the rows of data from the database.
def download_raw_housing_data(connection) -> pd.DataFrame:
    """
    Queries the database and returns all the raw house data for preprocessing module
    :param connection: accepts a sqlite3 Connection
    :return: pandas DataFrame containing the raw house data
    """
    sql = "SELECT * FROM kc_housing_data_raw"
    df = pd.read_sql(sql, connection, index_col='id')
    return df


def download_housing_data(connection) -> pd.DataFrame:
    """
    Queries the database and returns the house data from the table that contains the cleaned and preprocessed data
    :param connection: accepts a sqlite3 Connection
    :return: pandas DataFrame containing the processed house data
    """
    sql = 'SELECT * FROM house_data_processed'
    df = pd.read_sql(sql, connection, index_col='id')
    return df


def upload_processed_data(dataframe, connection):
    """
    Uploads the preprocessed data into the database
    :param dataframe: A DataFrame containing the processed data
    :param connection: A Connection object to the database
    """
    dataframe.to_sql('house_data_processed', connection, if_exists='replace')
    connection.commit()


def register_user(username, password, connection):
    """
    Registers a new user to the program
    :param username: identifies the user
    :param password: a unique pass phrase
    :param connection: a sqlite3 Connection object
    """
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO users(username, password, user_type) VALUES('{username}', '{password}', 'user')")
    connection.commit()

def save_prediction(dataframe):
    dataframe.to_sql('saved_predictions')


def login_user(username, password, connection):
    """
    Log the user into the program if they have a valid login.
    :param username: a users username
    :param password: a users password
    :param connection: a connection object.
    :return: the bool validity of the login.
    """
    query_result = pd.read_sql(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'",connection)

    # The password fails if the username and login are not valid int he database.
    if query_result.empty:
        return False  # return false when the result is empty.
    else:
        return True  # return true when the result is matched.

def submit_error_report(report, data_err, UI_err, func_err, connection):
    """
    Registers a new user to the program
    :param report: the information of the error report
    :param data_err: a unique tag for if its a data error
    :param UI_err: a unique tag for if its a UI error
    :param func_err: a unique tag for if its a functionality error
    :param connection: a sqlite3 Connection object
    """
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO error_reports(report, data_err, UI_err, func_err) VALUES('{report}', {data_err},"
                   f"{UI_err},{func_err})")
    connection.commit()
    connection.close()

def download_saved_data(connection) -> pd.DataFrame:
    """
    Queries the database and returns the house data from the table that contains the cleaned and preprocessed data
    :param connection: accepts a sqlite3 Connection
    :return: pandas DataFrame containing the processed house data
    """
    sql = 'SELECT * FROM saved_price_predictions'
    df = pd.read_sql(sql, connection, index_col='id')
    return df

def insert_data_into_saved(bedrooms, bathrooms, sqft_living, floors, waterfront, view, grade,
                                          sqft_basement, yr_built, yr_renovated, lat, long, price):
    """
    :param bedrooms:
    :param bathrooms:
    :param sqft_living:
    :param floors:
    :param waterfront:
    :param view:
    :param grade:
    :param sqft_basement:
    :param yr_built:
    :param yr_renovated:
    :param lat:
    :param long:
    :param price:
    :return:
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO saved_price_predictions('
                       f'bedrooms ,bathrooms, sqft_living, floors, waterfront, view, grade, sqft_basement,'
                       f'yr_built, yr_renovated, lat, long, price) VALUES ( {bedrooms}, {bathrooms}, {sqft_living},'
                   f' {floors}, {waterfront}, {view}, {grade}, {sqft_basement}, {yr_built}, {yr_renovated}, '
                   f'{lat}, {long}, "{price}")')
    connection.commit()
    connection.close()