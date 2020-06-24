import subprocess
import numpy as np
import os

print(os.getcwd())

for i in range(10):
    for rate in [0.3, 0.7]:

        subprocess.run(['ffmpeg', '-i', f'seperate_{i}/rate_{rate}_img/%03d.png', '-pix_fmt', 'yuv420p', f'seperate_{i}/rate_{rate}.mp4'])
