# Create mp4 of the images of a measurement
# i the number of different iterations that have been done (or the number at the end of the file map name "name_*")
# rate the range of rates which have been used inside the map file

import subprocess
import numpy as np

# Change range for i and rate as needed
for i in range(10):
    for rate in np.arange(1.1, 1.51, 0.1):
        rate = rate.round(1)
        subprocess.run(['ffmpeg', '-i', f'seperate_2_{i}/rate_{rate}_img/%03d.png', '-pix_fmt', 'yuv420p', f'seperate_2_{i}/rate_{rate}.mp4'])
