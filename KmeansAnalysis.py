"""
KmeansAnalysis handles the processed data from the database and runs a K-means clustering analaysis
to see different groups in the house data.
"""
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
import DatabaseConnection as dc

# Connect to database and get the data
home_data = dc.download_housing_data(dc.connect())

# Filter out outliers in the dataset based on the outlier graph from preprocessing
# indicating that the majority of the data is in the lower end of the price range.
home_data = home_data[home_data['price'] < 1250000]

# Visualize the different groupings of houses in the dataset using kmeans cluster analysis.
cata_home_data = home_data.copy() # copy of the dataset to maintain integrity
price_data = cata_home_data['price']
cata_home_data.drop(['price'],axis=1,inplace=True)

# Standardize the data.
scaler = StandardScaler()
scaler.fit(cata_home_data)
scaled_data = scaler.transform(cata_home_data)

# Determine the obtimal number of clusters
def show_elbow_plot():
    """
    Displays the elbow graph used to choose the optimal number of clusters for the final cluster graph.
    """

    test_cluster_max = 15
    kmeans_tests = [KMeans(n_clusters=i) for i in range(1, test_cluster_max)]
    score = [kmeans_tests[i].fit(scaled_data).score(scaled_data) for i in range(len(kmeans_tests))]

    # Plot the curve
    elbow_plot = plt.plot(range(1, test_cluster_max),score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve')
    plt.show()

def get_clustering_plot(hue_choice):
    """
    Creates and returns a seaborn scatterplot of the differnt clusters apparent in the data after the K-Means
    analysis.
    :return: a Seaborn scatter plot figure object
    """
    # Initialize the kmeans clustering algorithm
    kmeans = KMeans(n_clusters=8,init='k-means++')

    # Fit the data to the algo
    kmeans.fit(scaled_data)

    # Get the clusters
    labels = kmeans.predict(scaled_data)

    # Convert the data points into two dimensions
    pca = PCA(2)
    scaled_data_2d = pca.fit_transform(scaled_data)
    # scaled_data_2d = scaled_data

    #choose which labels to give the color choose
    hues = {'price': {'data':home_data['price'], 'huemap':'hot'}, 'clusters':{'data':labels, 'huemap':'rainbow'}}

    # Plot the data
    plt.figure(figsize=(12,12))
    cluster_plot = sns.scatterplot(x=scaled_data_2d[:, 0], y=scaled_data_2d[:, 1], hue=hues[hue_choice]['data'], palette=hues[hue_choice]['huemap']).get_figure()
    return cluster_plot

