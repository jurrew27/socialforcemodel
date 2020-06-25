import subprocess
import numpy as np

for i in range(10):
    for rate in np.arange(1.1, 1.51, 0.1):
        rate = rate.round(1)
        subprocess.run(['ffmpeg', '-i', f'seperate_2_{i}/rate_{rate}_img/%03d.png', '-pix_fmt', 'yuv420p', f'seperate_2_{i}/rate_{rate}.mp4'])
