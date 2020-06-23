import numpy as np
import pandas as pd
import math
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import os

# Change to work universally
os.chdir("C:/Users/hansp/Desktop/School/Master/Complex_system_simulation/Project/")


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

        clustering = DBSCAN(eps=0.6, min_samples=2, n_jobs=-1)
        fit_0 = clustering.fit_predict(data_points_0)
        fit_1 = clustering.fit_predict(data_points_1)

        plt.scatter(data_points_0[:, 0], data_points_0[:, 1], c=fit_0, marker="o", cmap="hot")
        plt.scatter(data_points_1[:, 0], data_points_1[:, 1], c=fit_1, marker="^", cmap="cool")
        plt.xlim(0, 30)
        plt.ylim(0, 5)
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
