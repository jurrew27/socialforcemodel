import socialforcemodel as sfm
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from multiprocessing import Pool

def main(args, iteration):
    out_dir = f'{args.outfile}_{iteration}'

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for rate in args.rates:
        out_dir_img = f'{out_dir}/rate_{rate}_img'

        if not os.path.exists(out_dir_img):
            os.makedirs(out_dir_img)

        loader = sfm.ParameterLoader(args.file)
        world = loader.world
        world.update()

        log_interval = 0.1
        log_every = round(log_interval / world.step_size)

        for group in world.groups:
            group.set_ornstein_uhlenbeck_process(0, 0.15, 0.01)
            group.set_spawn_rate(rate)

        rows = []

        for step in tqdm(range(args.steps), desc=f'Iteration {iteration}, rate {rate}'):
            if not world.step():
                break

            world.update()
            if step % log_every == 0:
                figure = world.plot()
                figure.savefig(f'{out_dir_img}/%03d.png' % ((step + 1) // log_every),
                               bbox_inches = 'tight',
                               pad_inches = 0.1)
                figure.clear()
                plt.close(figure)

            if step % log_every == 0:
                pedestrians = world.quadtree.get_pedestrians()
                for p in pedestrians:
                    rows.append([world.time, p.id, p.group.id, p.position[0], p.position[1], p.speed])

        with open(f'{out_dir}/rate_{rate}.csv', 'w') as outfile:
            import csv
            writer = csv.writer(outfile)
            writer.writerow(['time', 'pedestrian_id', 'group_id', 'x', 'y', 'velocity'])
            for row in rows:
                writer.writerow(row)


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

    with Pool() as p:
        p.starmap(main, zip([args]*args.iterations, range(args.iterations)))