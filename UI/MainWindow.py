"""
The primary User Interface module that handles different tabs of graphs and interactive elements.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import DataPreprocessing as dpp
import DatabaseConnection as dc
import KmeansAnalysis
from RegressionPrediction import PredictionTrainer


def create_note_page(master, name):
    """
    Creates a new tab note page in the notebook.
    :param master: the root element of this page should be the Notebook
    :param name: the Name for the note page
    :return: the Frame containing the note page
    """
    frame = ttk.Frame(master)
    master.add(frame, text=name)
    tab_content_lbl = ttk.Label(frame, text=name, style='NB.Title.Label')
    tab_content_lbl.pack(pady=(20, 20))

    return frame


def create_description(master, text):
    """
    Create a scaling description text field to hold some information about the various graphs and interactive elements.
    :param master: the parent of the description should be the note page.
    :param text: The text of the description.
    """
    text_area = tk.Text(master)
    text_area.insert(tk.END, text)
    text_area.configure(state='disabled', relief=tk.FLAT, font=('Arial', 18))
    text_area.pack()

    return text_area


def display_plot(master_frame, plot):
    """
    Displays a figure plot in a tkinter canvas.
    :param master_frame: the parent frame of the plot
    :param plot: the plot to be displayed
    """

    canvas = FigureCanvasTkAgg(plot, master=master_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True)

    return canvas


def display_price_regression(master_frame, regressor):
    """
    Create and display the tab of the notebook that contains the price prediction regression line and the scored metrics
    of accuracy r^2 score and mean absolute error.
    :param master_frame: the parent frame
    :param regressor: the regression object created in RegressionPrediction module.
    """

    reg_plot_tab = create_note_page(master_frame, "Regression Plot Price")
    # The price regression plot
    predict_plot_frame = ttk.Frame(reg_plot_tab)
    reg_plot = regressor.get_reg_pred_prices()  # The price regression plot
    display_plot(predict_plot_frame, reg_plot)  # Display the plot
    predict_plot_frame.pack(side='left')

    # The text area describing the plot and the metrics of accuracy
    predict_plot_text_frame = ttk.Frame(reg_plot_tab)
    # Price prediction accuracy values for display
    mean_error_actual = "${:,.2f}".format(regressor.maerr)
    percent_acc = round(regressor.r2 * 100)
    # Text to be displayed in the text area
    predict_desc = f'The program predicts the price with a {percent_acc}% accuracy. \n' \
                   f'The mean real value difference between predicted price and real price is {mean_error_actual}.'
    create_description(predict_plot_text_frame, predict_desc)
    predict_plot_text_frame.pack(side='left', padx=(100, 0))


def display_house_clusters(master_frame):
    """
    Creates and displays the house clusters tab of the dash, which has the cluster plot.
    :param master_frame: the parent frame of this tab
    """
    house_clusters = create_note_page(master_frame, "House Clusters")
    # Create a space for the plot
    cluster_plot_frame = ttk.Frame(house_clusters)
    cluster_plot_frame.pack(side='left')

    # Pick the hue map
    choose_hue_var = tk.StringVar()
    choose_hue_var.set('clusters')

    # Display the plot
    cluster_plot = KmeansAnalysis.get_clustering_plot(choose_hue_var.get())
    display_plot(cluster_plot_frame, cluster_plot)


def display_data_analysis(master_frame):
    """
    Creates and displays the data analysis tab of the notebook.
    :param master_frame: the parent frame of the page
    """
    data_analysis = create_note_page(master_frame, "Data Analysis")

    # Create  and display the plots
    corr_and_outlier = dpp.create_plots()
    corr_and_outlier_frame = ttk.Frame(data_analysis)
    corr_and_outlier_frame.pack(side='left', padx=(100, 0))
    display_plot(corr_and_outlier_frame, corr_and_outlier)

    # Create and display the text describing the plots
    text_frame = ttk.Frame(data_analysis)
    data_analysis_description = 'The raw data is analyzed using correlation coefficient between the price of the ' \
                                'house and the other features in the data. The higher the number the more important ' \
                                'the feature.' \
                                '\n' \
                                '\n' \
                                'Next the outliers in the price data are graphed so that the KMeans learning model ' \
                                'can be filtered properly.'

    create_description(text_frame, data_analysis_description)
    text_frame.pack(side='left', padx=(100, 0))


def display_prediction_engine(master_frame, current_window, regressor):
    """
    Creates and displays the prediction engine that allows users to enter house features and get predicted house prices.
    :param master_frame: the parent frame of the note page
    :param current_window: the main window of the program; used to register the form validation functions
    :param regressor: a regressor that can make predictions about the house price
    """
    prediction_engine = create_note_page(master_frame, "Price Prediction Engine")

    fields_frame = ttk.Frame(prediction_engine)
    fields_frame.pack(side='left', padx=(200, 200))

    # These functions handle the field values validation; prevents incorrect entries by preventing input
    # or by validating the input against a range of allowed values.

    # The number of bedrooms and bathrooms but be between 0 and 10
    def callback_bed_bath(cascade_input):
        if cascade_input.isdigit():
            if 0 <= float(cascade_input) <= 10:
                return True
            else:
                return False
        elif cascade_input == "":
            return True
        else:
            return False

    # The square footage of the living space must be between 0 and 100,000 sqft
    def callback_sqft(cascade_input):
        if cascade_input.isdigit():
            if 0 <= float(cascade_input) <= 100000:
                return True
            else:
                return False
        elif cascade_input == "":
            return True
        else:
            return False

    # The number of times the property has been viewed must be between 0 and 100 times
    def callback_views(cascade_input):
        if cascade_input.isdigit():
            if 0 <= float(cascade_input) <= 100:
                return True
            else:
                return False
        elif cascade_input == "":
            return True
        else:
            return False

    # For the latitude and longitude the values are within the United States roughly
    # The valid range for latitude values is between 28 and 48
    def callback_lat(cascade_input):
        invalid_msg = "latitude invalid: must be between 28.000000 and 48.000000"
        try:
            latitude = float(cascade_input)
        except:
            latitude = 0
            lat_valid_var.set(invalid_msg)
        if 28.0 <= latitude <= 48.0:
            lat_valid_var.set('valid')
            return True
        elif cascade_input == "":
            return True
        else:
            lat_valid_var.set(invalid_msg)
            return True

    # The valid range for longitude values is between 67 and 124 the function handles
    # making it negative
    def callback_long(cascade_input):
        invalid_msg = "longitude invalid: must be between -67.000000 and -124.000000"
        try:
            longitude = float(cascade_input)
        except:
            longitude = 0
            long_valid_var.set(invalid_msg)
        if -124.0 <= -longitude <= -67.0:
            long_valid_var.set("valid")
            return True
        elif cascade_input == "":
            return True
        else:
            long_valid_var.set(invalid_msg)
            return True

    # Register the callback methods to the window
    reg_call_bnb = current_window.register(callback_bed_bath)
    reg_call_sqft = current_window.register(callback_sqft)
    reg_call_views = current_window.register(callback_views)
    reg_call_lat = current_window.register(callback_lat)
    reg_call_long = current_window.register(callback_long)

    # Bedrooms field
    bedrooms_lbl = ttk.Label(fields_frame, text='bedrooms (10 max)')
    bedrooms_entry = ttk.Entry(fields_frame, validate='key', validatecommand=(reg_call_bnb, '%P'))
    bedrooms_entry.insert(tk.END, 1)
    bedrooms_lbl.pack()
    bedrooms_entry.pack()

    # Bathrooms field
    bathrooms_lbl = ttk.Label(fields_frame, text='bathrooms (10 max)')
    bathrooms_entry = ttk.Entry(fields_frame, validate='key', validatecommand=(reg_call_bnb, '%P'))
    bathrooms_entry.insert(tk.END, 1)
    bathrooms_lbl.pack()
    bathrooms_entry.pack()

    # Sqft living field
    sqft_living_lbl = ttk.Label(fields_frame, text='sqft living area (100000 max)')
    sqft_living_lbl.pack()
    sqft_living_entry = ttk.Entry(fields_frame, validate='key', validatecommand=(reg_call_sqft, '%P'))
    sqft_living_entry.insert(tk.END, 1000)
    sqft_living_entry.pack()

    # Floors field
    floors_lbl = ttk.Label(fields_frame, text='floors (1-4 floors)')
    floors_lbl.pack()
    floors_picker = ttk.Spinbox(fields_frame, values=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0], wrap=True, state='readonly')
    floors_picker.set(1.0)
    floors_picker.pack()

    # Waterfront field
    waterfront_lbl = ttk.Label(fields_frame, text='waterfront (present = 1 not = 0')
    waterfront_lbl.pack()
    waterfront_picker = ttk.Spinbox(fields_frame, values=[1, 0], wrap=True, state='readonly')
    waterfront_picker.set(0)
    waterfront_picker.pack()

    # Views field
    view_lbl = ttk.Label(fields_frame, text='views (number of times the property was viewed 100 max)')
    view_lbl.pack()
    view_entry = ttk.Entry(fields_frame, validate='key', validatecommand=(reg_call_views, '%P'))
    view_entry.insert(tk.END, 0)
    view_entry.pack()

    # House grade field
    grade_lbl = ttk.Label(fields_frame, text='grade (materials and craftsmanship 1-13 scale)')
    grade_lbl.pack()
    grade_picker = ttk.Spinbox(fields_frame, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], wrap=True,
                               state='readonly')
    grade_picker.set(7)
    grade_picker.pack()

    # Sqft basement field
    sqft_basement_lbl = ttk.Label(fields_frame, text='sqft basement (100000 max)')
    sqft_basement_lbl.pack()
    sqft_basement_entry = ttk.Entry(fields_frame, validate='key', validatecommand=(reg_call_sqft, '%P'))
    sqft_basement_entry.insert(tk.END, 0)
    sqft_basement_entry.pack()

    # Year built field
    yr_built_lbl = ttk.Label(fields_frame, text='year built (1800-present)')
    yr_built_lbl.pack()
    years = []
    for i in range(1800, 2021):
        years.append(i)

    yr_built_picker = ttk.Combobox(fields_frame, values=years, state='readonly')
    yr_built_picker.set(1979)
    yr_built_picker.pack()

    # Year renovated field
    years.insert(0, 0)
    yr_renovated_lbl = ttk.Label(fields_frame, text='year renovated (0 = not renovated, 1800-present)')
    yr_renovated_lbl.pack()
    yr_renovated_picker = ttk.Combobox(fields_frame, values=years, state='readonly')
    yr_renovated_picker.set(0)
    yr_renovated_picker.pack()

    # Latitude field
    lat_lbl = ttk.Label(fields_frame, text='latitude (between 28.0 and 48.0)')
    lat_entry = ttk.Entry(fields_frame, validate='key', validatecommand=(reg_call_lat, '%P'))
    lat_lbl.pack()
    lat_entry.pack()
    lat_valid_var = tk.StringVar()
    lat_valid_var.set("invalid")
    lat_valid_lbl = ttk.Label(fields_frame, textvariable=lat_valid_var)
    lat_valid_lbl.pack()

    # Longitude field
    long_lbl = ttk.Label(fields_frame, text='longitude (between 67.0 and 124.0)')
    long_lbl.pack()
    long_entry = ttk.Entry(fields_frame, validate='key', validatecommand=(reg_call_long, '%P'))
    long_entry.pack()
    long_valid_var = tk.StringVar()
    long_valid_var.set("invalid")
    long_valid_lbl = ttk.Label(fields_frame, textvariable=long_valid_var)
    long_valid_lbl.pack()

    # The output of the prediction
    output_frame = ttk.Frame(prediction_engine)
    output_frame.pack(side='left')
    price_predicted_var = tk.StringVar()
    price_predicted_var.set("House Price:")
    price_predicted_lbl = ttk.Label(output_frame, textvariable=price_predicted_var)

    def submit():
        """
        Function command for the predict button that collects and provides final validation before prediction occurs.
        """
        lat_valid = str(lat_valid_var.get())
        long_valid = str(long_valid_var.get())

        # Only performs the prediction if the lat and long are valid
        if lat_valid == 'valid' and long_valid == 'valid':
            bedrooms = float(bedrooms_entry.get())
            bathrooms = float(bathrooms_entry.get())
            sqft_living = float(sqft_living_entry.get())
            floors = float(floors_picker.get())
            waterfront = float(waterfront_picker.get())
            view = float(view_entry.get())
            grade = float(grade_picker.get())
            sqft_basement = float(sqft_basement_entry.get())
            yr_built = int(yr_built_picker.get())
            yr_renovated = int(yr_renovated_picker.get())
            lat = float(lat_entry.get())
            long = float(long_entry.get())
            fields_list = [bedrooms, bathrooms, sqft_living, floors, waterfront, view, grade, sqft_basement, yr_built,
                           yr_renovated, lat, long]

            price = regressor.predict_house_price(fields_list)
            price_var = "House Price: ${:,.2f}".format(price)
            price_predicted_var.set(price_var)
        else:
            not_valid = 'All fields must be valid for a prediction'
            price_predicted_var.set(not_valid)

    # The predict button that executes the prediction functions
    predict_btn = ttk.Button(fields_frame, text="predict price", command=submit)
    predict_btn.pack()
    price_predicted_lbl.pack()

    def save():
        """
        Function command for the save button that collects the data to be sent to the database.
        Mirrors some of the functionality of predict to ensure that the validation occurs at each stage and
        that no bad data gets submitted.
        """
        lat_valid = str(lat_valid_var.get())
        long_valid = str(long_valid_var.get())

        # Only performs the prediction if the lat and long are valid
        if lat_valid == 'valid' and long_valid == 'valid':
            bedrooms = float(bedrooms_entry.get())
            bathrooms = float(bathrooms_entry.get())
            sqft_living = float(sqft_living_entry.get())
            floors = float(floors_picker.get())
            waterfront = float(waterfront_picker.get())
            view = float(view_entry.get())
            grade = float(grade_picker.get())
            sqft_basement = float(sqft_basement_entry.get())
            yr_built = int(yr_built_picker.get())
            yr_renovated = int(yr_renovated_picker.get())
            lat = float(lat_entry.get())
            long = float(long_entry.get())
            fields_list = [bedrooms, bathrooms, sqft_living, floors, waterfront, view, grade, sqft_basement, yr_built,
                           yr_renovated, lat, long]

            price = regressor.predict_house_price(fields_list)

            price_var = "House Price: ${:,.2f}".format(price)

            price_predicted_var.set(price_var)
            if price:
                dc.insert_data_into_saved(bedrooms, bathrooms, sqft_living, floors, waterfront, view, grade,
                                          sqft_basement, yr_built, yr_renovated, lat, long, price)
                messagebox.showinfo("alert", "price was saved")

        else:
            not_valid = 'All fields must be valid for a prediction'
            price_predicted_var.set(not_valid)

    save_btn = ttk.Button(fields_frame, text="save price", command=save)
    save_btn.pack()


def display_saved_data(master_frame):
    """
    Creates and displays the data saved from the database of the predicted prices.
    :param master_frame: the parent frame notebook
    """
    data_view = create_note_page(master_frame, 'Data Manager')

    data_table = tk.Listbox(data_view)
    data_table.pack(side='left', fill='both', expand=True)
    scrollbar = ttk.Scrollbar(data_view)
    scrollbar.pack(side='right', fill='both')
    data_table.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=data_table.yview)

    def query_saved_data():
        data_table.delete(0, tk.END)
        data = dc.download_saved_data(dc.connect())
        for index, row in data.iterrows():
            data_row = (
                f"bedrooms: {row['bedrooms']} "
                f"bathrooms: {row['bathrooms']} "
                f"sqft_living: {row['sqft_living']} "
                f"floors: {row['floors']} "
                f"waterfront: {row['waterfront']} "
                f"view: {row['view']} "
                f"grade: {row['grade']} "
                f"sqft_basement: {row['sqft_basement']} "
                f"yr_built: {row['yr_built']} "
                f"yr_renovated: {row['yr_renovated']} "
                f"lat: {row['lat']} "
                f"long: {row['long']} "
                f"price: ${row['price']} "
                )
            data_table.insert(tk.END, data_row)

    query_house_data_btn = ttk.Button(data_view, text='view saved price predictions', command=query_saved_data)
    query_house_data_btn.pack()


def display_debug(master_frame):
    """
    Creates and displays the debug options for the application should data anomalies become present.
    :param master_frame: the parent frame
    """
    maintenance = create_note_page(master_frame, "Maintenance")

    # Report an error to the database to be read by the product managers
    report_options = ttk.Frame(maintenance)
    report_options.pack()

    data_error_var = tk.IntVar()
    data_error = ttk.Checkbutton(report_options, text='data error', variable=data_error_var)
    data_error.pack(side='left')

    UI_error_var = tk.IntVar()
    UI_error = ttk.Checkbutton(report_options, text='user interface error', variable=UI_error_var)
    UI_error.pack(side='left')

    function_error_var = tk.IntVar()
    function_error = ttk.Checkbutton(report_options, text='function error', variable=function_error_var)
    function_error.pack(side='left')

    report_error_text = create_description(maintenance, 'please describe your error')
    report_error_text.configure(state='normal', width=50, height=10, font=('Arial', 11))

    def submit_err():
        """submit the error reports"""
        report = report_error_text.get("1.0",tk.END)
        de = data_error_var.get()
        ue = UI_error_var.get()
        fe = function_error_var.get()
        dc.submit_error_report(report,de,ue,fe,dc.connect())
        messagebox.showinfo("info", "thank you for reporting errors")

    report_error = ttk.Button(maintenance, text='submit error report', command=submit_err)
    report_error.pack()
    report_error_lbl = ttk.Label(maintenance, text='report an error in the program')
    report_error_lbl.pack()

    # Reset the data in the database using the original data and reprocessing it
    def reset_data():
        dpp.upload_to_db_post_processed_data()
        messagebox.showwarning("Data Reset", "data has been reset")

    # Reset button to reset the database data
    reset_data_btn = ttk.Button(maintenance, text='reset data', command=reset_data)
    reset_data_btn.pack()
    reset_lbl = ttk.Label(maintenance, text='reset the processed data')
    reset_lbl.pack()


def start(window, loading_bar):
    """Starts up the main window part of the application after validation from the login screen
        includes a progress bar as each component loads.
    """
    regression_training = PredictionTrainer()

    # Settings for this window
    style = ttk.Style()
    style.configure('TNotebook', tabposition='n', font=('Arial', 18))
    style.configure('NB.Title.Label', font=('Arial', 25))
    tab_control = ttk.Notebook(window)  # Create a new tab menu notebook

    # Create the sections of the notebook
    # Tab 1 is the price dashboard with the display predicted price regression plot and the display of the
    # predicted accuracy
    display_price_regression(tab_control, regression_training)
    loading_bar.step(20)
    loading_bar.update_idletasks()
    # Tab 2 is the cluster analysis through k-means and graphing with a seaborn scatter plot
    display_house_clusters(tab_control)
    loading_bar.step(10)
    loading_bar.update_idletasks()
    # Tab 3 is the data analysis booklet with the graphs of raw data that describe how the data mining choices were made
    display_data_analysis(tab_control)
    loading_bar.step(10)
    loading_bar.update_idletasks()
    # Tab 4 is an interactive prediction engine that gives a guess at the price for a set of features
    display_prediction_engine(tab_control, window, regression_training)
    loading_bar.step(10)
    loading_bar.update_idletasks()
    # Tab 5 contains saved price predictions in the database
    display_saved_data(tab_control)
    loading_bar.step(10)
    loading_bar.update_idletasks()
    # Tab 6 program maintenance and debugging
    display_debug(tab_control)
    loading_bar.step(10)
    loading_bar.update_idletasks()

    tab_control.pack(expand=1, fill="both")

    # Update the progress bar as the window loads
    loading_bar.step(10)
    loading_bar.update_idletasks()
    loading_bar.pack_forget()

    return window
