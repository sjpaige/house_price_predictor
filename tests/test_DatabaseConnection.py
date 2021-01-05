from unittest import TestCase
import pandas
import sqlite3

import DatabaseConnection as dc

connection = dc.connect()  # Create a connection to the db


class DatabaseConnectionUnitTests(TestCase):
    """
    The unit tests for the DatabaseConnection module.
    """

    # Tests to make sure that the connection is the correct object
    def test_connect_to_database(self):
        self.assertTrue(isinstance(connection, sqlite3.Connection))

    # Tests that the raw data can be downloaded in the correct format and size
    def test_download_raw_housing_data_from_database(self):
        df = dc.download_raw_housing_data(connection)

        self.assertTrue(isinstance(df, pandas.DataFrame))  # Must be a DataFrame
        self.assertGreaterEqual(len(df), 20000)  # Must have around the amount of data in the table

    # Tests that the processed data can be downloaded in the correct format and size
    def test_download_housing_data_from_database(self):
        df = dc.download_housing_data(connection)

        self.assertTrue(isinstance(df, pandas.DataFrame))  # Must be a DataFrame
        self.assertGreaterEqual(len(df), 15000)  # Must have around the amount of data in the table

    # Tests that the data can be uploaded successfully
    def test_upload_processed_data(self):
        # If downloading raw housing data is working then the upload was successful
        self.test_download_housing_data_from_database()

    # Registers a user with the database and compares to the original data
    def test_register_user_into_db(self):
        username_test = 'test1111XXX'
        password_test = 'test1111AAA'

        cursor = connection.cursor()  # Connect to database
        dc.register_user(username_test, password_test, connection)  # Register a test user

        test_params = [(username_test, password_test)]  # Format the test data for comparison
        # Obtain the data of the test user from the database and save into a variable
        data_from_db = cursor.execute(
            f"SELECT username, password FROM users WHERE username = '{username_test}'").fetchall()
        cursor.execute(f"DELETE FROM users WHERE username = '{username_test}'")  # Remove the test data from the db
        connection.commit()  # Commit changes to database

        # Compare the saved original data to the database obtained data
        self.assertEqual(test_params, data_from_db)
