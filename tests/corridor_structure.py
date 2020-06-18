import socialforcemodel as sfm
import matplotlib.pyplot as plt
import os
from tqdm import tqdm


def main(args):
    if not os.path.exists("img"):
        os.makedirs("img")
    if not os.path.exists("measurements"):
        os.makedirs("measurements")

    for rate in args.rates:
        if not os.path.exists("img/rate_{}".format(rate)):
            os.makedirs("img/rate_{}".format(rate))

        loader = sfm.ParameterLoader(args.file)
        world = loader.world
        world.update()

        log_interval = 0.1
        log_every = round(log_interval / world.step_size)

        for group in world.groups:
            group.set_ornstein_uhlenbeck_process(0, 0.15, 0.01)
            group.set_spawn_rate(rate)

        rows = []

        for step in tqdm(range(args.steps), desc=f'Rate {rate}'):
            if not world.step():
                break

            world.update()
            if step % log_every == 0:
                figure = world.plot()
                figure.savefig("img/rate_{}/%03d.png".format(rate) % ((step + 1) // log_every),
                               bbox_inches = 'tight',
                               pad_inches = 0.1)
                figure.clear()
                plt.close(figure)

            if step % log_every == 0:
                pedestrians = world.quadtree.get_pedestrians()
                for p in pedestrians:
                    rows.append([world.time, p.id, p.group.id, p.position[0], p.position[1], p.speed])

        with open("{}/rate_{}.csv".format(args.outfile, rate), "w") as outfile:
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
    args = parser.parse_args(sys.argv[1:])
    main(args)