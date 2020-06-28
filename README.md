This repository contains the code for the project fo the Complex System Simulation course of the University of Amsterdam by Hans
 Pijpers and Jurre Wolsink. It implements the Helbing-Molnár-Farkas-Vicsek Social Force Model package made by Rex Valkering. 


### Requirements

- Numpy
- Scipy
- Matplotlib
- PyYAML
- TQDM
- Pympler
- Psutil
- Numba


### Usage

```python simulate.py <config_file (string)> -s --steps <int> -r --rates <float>, <float>, ... -i --iterations <int> -o --output <string>```

For example:

```python simulate.py collisioncorridor.yaml -s 10 -r 0.1 0.2 0.3 -i 2 -o test_run```

### YAML config files

You can use a .yaml parameter file to load and build a world. The following parameters are configurable:

##### Global parameters

* `world_width` (*float*) - default `10.0` - width (x) of domain
* `world_height` (*float*) - default `10.0` - height (y) of domain
* `continuous_domain` (*boolean*) - default `False` - whether the domain should wrap around
* `step_size` (*float*) - default `0.05` - simulation step size
* `default_desired_velocity` (*float*) - default `1.3` - default desired velocity of pedestrians
* `default_maximum_velocity` (*float*) - default `2.6` - default maximum velocity of pedestrians
* `default_relaxation_time` (*float*) - default `2.0` - default relaxation time of pedestrians
* `desired_velocity_importance` (*float*) - default `0.8` - between 0.0 and 1.0, lower means the velocity is more dependent on neighbourhood velocity
* `interactive_distance_threshold` (*float*) - default `2.0` - distance after which objects and pedestrians are no longer used in interactive force calculations
* `target_distance_threshold` (*float*) - default `0.13` - maximum distance to target for it to be considered reached
* `repulsion_coefficient` (*float*) - default `2000 Newton`
* `falloff_length` (*float*) - default `0.08 meters`
* `body_force_constant` (*float*) - default `12000 kg / s²`
* `friction_force_constant` (*float*) - default `24000 kg / ms`
* `quad_tree_threshold` (*integer*) - maximum number of pedestrians in a quad tree leaf
* `groups` (one or more *Group* entities) - pedestrian groups in this simulation
* `obstacles` (one or more *Obstacle* entities) - obstacles in this simulation

##### Entity variables

###### Point:
* `x` (*float*)
* `y` (*float*)

###### Area:
* `start` (*Point*)
* `end` (*Point*)
    
###### Group:
Default values are taken from global variables if not provided.
* `start_time` (*float*) - default `0 seconds` - Time at which this group should appear in the simulation
* `spawn_area` (*Area*) - The default area in which new pedestrians should spawn
* `spawn_rate` (*float*) - default `0 pedestrians per second` - Pedestrian spawn rate
* `target_area` (*Area*) - The default area in which new pedestrian targets should spawn
* `target_path` (one or more *Point* entities) - The path which pedestrians should follow to get to their target
* `mass` (*float*) - default `60 kg` - Mass of pedestrians
* `radius` (*float*) - default `0.15 m` - Radius of pedestrians
* `desired_velocity` (*float*) - Desired velocity of pedestrians
* `maximum_velocity` (*float*) - Maximum velocity of pedestrians
* `relaxation_time` (*float*) - Relaxation time of pedestrians
* `num_pedestrians` (*integer*) - The number of pedestrians to spawn with default parameters
* `pedestrians` (one or more *Pedestrian* entities) - Pedestrians to add to this group

###### Pedestrian:
Pedestrians should always be part of a group. Variables that are not set are inferred from the group.
* `start` (*Point*) - Spawn point
* `target` (*Point*) - Target point
* `target_path` (one or more *Point* entities) - The path which this pedestrian should follow to get to their target.
* `mass` (*float*) - Mass of pedestrian
* `radius` (*float*) - Radius of pedestrian
* `desired_velocity` (*float*) - Desired velocity of pedestrian
* `maximum_velocity` (*float*) - Maximum velocity of pedestrian
* `relaxation_time` (*float*) - Relaxation time of pedestrian

###### Obstacle:
* `points` (one or more *Point* entities) - series of points. Line segments are drawn between pairs of points.
