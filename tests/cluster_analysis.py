# Cluster analysis which should find the size and amount of "trains" in the group
# Code calculates the wrong clusters and cannot find the trains
# DBSCAN and GaussianMixture clustering methods have been tried and both have failed
# For GaussianMixture, multiple amount of clusters have been tried and compared but none worked correct

# To run, add csv-file of a measurement in the commandline

import numpy as np
import pandas as pd
import math
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

def analyze_data(args):
    df = pd.read_csv(args.file, sep=",")
    # Eliminate trailing zeroes from floats in time
    df.time = df.time.round(2)

    # Calculate cluster every 10 time units
    for t in np.arange(9.95, 100, 10):
        # Create temporary dataframe with the pedestrians at t for group 0
        temp_df_0 = df.loc[((df['time'] == t) & (df['group_id'] == 0))]

        data_points_0 = np.column_stack([temp_df_0.x.values, temp_df_0.y.values])

        # Create temporary dataframe with the pedestrians at t for group 1
        temp_df_1 = df.loc[((df['time'] == t) & (df['group_id'] == 1))]
        data_points_1 = np.column_stack([temp_df_1.x.values, temp_df_1.y.values])

        #clustering = DBSCAN(eps=1, min_samples=2, algorithm="ball_tree")
        #fit_0 = clustering.fit_predict(data_points_0)
        #fit_1 = clustering.fit_predict(data_points_1)

        mixture = GaussianMixture(n_components=5, covariance_type='full')

        fit_0 = mixture.fit_predict(data_points_0)
        fit_1 = mixture.fit_predict(data_points_1)

        # Plot clusters
        plt.scatter(data_points_0[:, 0], data_points_0[:, 1], c=fit_0, marker="o", cmap="hot", label="group 1")
        ca = plt.colorbar()
        plt.scatter(data_points_1[:, 0], data_points_1[:, 1], c=fit_1, marker="^", cmap="cool", label="group 2")
        cb = plt.colorbar()
        plt.xlim(0, 30)
        plt.ylim(0, 5)
        ca.set_label("group 1")
        cb.set_label("group 2")
        plt.legend()

        plt.show()


def main(args):
    analyze_data(args)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='YAML-file')
    parser.add_argument('-o', '--outfile', help='File for measurements', default='measurements')
    args = parser.parse_args(sys.argv[1:])

    main(args)
