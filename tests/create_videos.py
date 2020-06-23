import subprocess
import numpy as np

for i in range(5):
    for rate in np.arange(0.1, 1.01, 0.1):
        subprocess.run(['ffmpeg', '-i',  f'measurements_{i}/rate_{rate}_img/%03d.png', '-pix_fmt', 'yuv420p', f'measurements_{i}/rate_{rate}.mp4'])