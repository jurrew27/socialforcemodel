# Simulates the social force model for the given parameters
# Iterations are run parallel on the threads available
# Initialize as: ".yaml file -s #steps -o name outfile -r all rates as e.g. 0.1 0.2 0.3 0.4 -i # iterations per rate"
# If only .yaml is given, standard values s=500, o="measurements", r=1, i=1 are used

import socialforcemodel as sfm
import matplotlib.pyplot as plt
import os
from tqdm import trange
from multiprocessing import Pool
from itertools import product
from functools import partial


def simulate(args, iteration, rate):
    loader = sfm.ParameterLoader(args.file)
    world = loader.world
    world.update()

    log_interval = 0.1
    log_every = round(log_interval / world.step_size)

    for group in world.groups:
        group.set_ornstein_uhlenbeck_process(0, 0.15, 0.01)
        group.set_spawn_rate(rate)

    rows = []

    for step in trange(args.steps, desc=f'Iteration {iteration}, rate {rate}'):
        if not world.step():
            break

        world.update()
        if step % log_every == 0:
            figure = world.plot()
            figure.savefig(f'{args.outfile}_{iteration}/rate_{rate}_img/%03d.png' % ((step + 1) // log_every),
                           bbox_inches='tight',
                           pad_inches=0.1)
            figure.clear()
            plt.close(figure)

            pedestrians = world.quadtree.get_pedestrians()
            for p in pedestrians:
                rows.append([world.time, p.id, p.group.id, p.position[0], p.position[1], p.speed])

    with open(f'{args.outfile}_{iteration}/rate_{rate}.csv', 'w') as outfile:
        import csv
        writer = csv.writer(outfile)
        writer.writerow(['time', 'pedestrian_id', 'group_id', 'x', 'y', 'velocity'])
        for row in rows:
            writer.writerow(row)


def main(args):
    for iteration in range(args.iterations):
        out_dir = f'{args.outfile}_{iteration}'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        for rate in args.rates:
            out_dir_img = f'{out_dir}/rate_{rate}_img'
            if not os.path.exists(out_dir_img):
                os.makedirs(out_dir_img)

    iterable = product(range(args.iterations), args.rates)
    with Pool() as p:
        p.starmap(partial(simulate, args), iterable)


if __name__ == '__main__':
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='YAML-file')
    parser.add_argument('-s', '--steps', help='Number of steps', type=int, default=500)
    parser.add_argument('-o', '--outfile', help='File for measurements', default='measurements')
    parser.add_argument('-r', '--rates', default=1, nargs='+', type=float),
    parser.add_argument('-i', '--iterations', help='Number of iterations', type=int, default=1)
    args = parser.parse_args(sys.argv[1:])

    main(args)