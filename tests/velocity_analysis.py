import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_data(args):
    mean_velocities = []
    for f in args.file:
        df = pd.read_csv(f, sep=",")
        # Eliminate trailing zeroes from floats in time
        df.time = df.time.round(2)

        # Calculate mean velocity each time step; start at 0.05 due to the csv file
        file_velocities = []
        for t in np.arange(0.05, 100, 0.1):
            temp_df = df.loc[df["time"] == np.round(t,2)]
            mean_velocity = temp_df.velocity.mean()

            # Save mean velocity
            file_velocities.append(mean_velocity)

        # Save all mean velocities over time
        mean_velocities.append(file_velocities)

    # Make numpy array for mean and std
    np_velocities = np.array(mean_velocities)
    total_mean_velocities = np.nanmean(np_velocities, axis=0)
    std_velocities = np.nanstd(np_velocities, axis=0)

    # plot it
    fig, ax = plt.subplots(1)
    ax.plot(np.arange(0.05, 100, 0.1), total_mean_velocities, color = 'black')
    ax.fill_between(np.arange(0.05, 100, 0.1), total_mean_velocities + std_velocities, total_mean_velocities - std_velocities, facecolor='red')
    ax.set_title(r'Mean velocities (rate=%g)' % args.rate)
    ax.legend(loc='upper left')
    ax.set_xlabel('t')
    ax.set_ylabel('velocity')
    ax.grid()

    plt.show()



    #with open(f'{args.outfile}_{iteration}/rate_{rate}.csv', 'w') as outfile:
    #    import csv
    #    writer = csv.writer(outfile)
    #    writer.writerow(['time', 'pedestrian_id', 'group_id', 'x', 'y', 'velocity'])
    #    for row in rows:
    #        writer.writerow(row)


def main(args):
    #out_dir = f'{args.outfile}_{args.iterations}'
    #if not os.path.exists(out_dir):
    #    os.makedirs(out_dir)

    analyze_data(args)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-files', '--file', nargs='+', help='YAML-file')
    parser.add_argument('-o', '--outfile', help='File for measurements', default='Velocity_analysis')
    parser.add_argument('-r', '--rate', default=1, type=float)
    parser.add_argument('-i', '--iterations', help='Number of iterations', type=int, default=1)
    args = parser.parse_args(sys.argv[1:])

    main(args)
