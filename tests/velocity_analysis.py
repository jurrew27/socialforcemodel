import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_data(args):
    mean_velocities = []
    for f in args.file:
        df = pd.read_csv(f, sep=",")
        df = calculate_real_velocities(args, df)
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

def calculate_real_velocities(args, data):

    for id_ped in range(data.pedestrian_id.min(), data.pedestrian_id.max()):

        temp_df = data.loc[data["pedestrian_id"] == id_ped]

        vec_x = temp_df['x'].values[1:]
        vec_old_x = temp_df['x'].values[:-1]
        vec_y = temp_df['y'].values[1:]
        vec_old_y = temp_df['y'].values[:-1]

        delta_x = abs(vec_x - vec_old_x)
        delta_y = abs(vec_y - vec_old_y)

        displacement = list(map(math.sqrt, delta_x**2 + delta_y**2))
        time_elapsed = temp_df['time'].values[1:] - temp_df['time'].values[:-1]
        proper_velocity = displacement / time_elapsed

        # Insert first value into list as workaround, as i cant get pandas to give me [1:] of the velocity list of the pedastrian
        proper_velocity = np.insert(proper_velocity, 0, temp_df['velocity'].values[0])

        data["velocity"].loc[data["pedestrian_id"] == id_ped] = proper_velocity

    return data

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
