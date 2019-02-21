"""
This plot shows the angle against time, along with the position of the robot against time.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.
"""

import numpy as np
from numpy import loadtxt
import os
import matplotlib.pyplot as plt
from graph_format import format_graph
from sys import path
path.insert(0, '..')
from utility_functions import read_file, convert_read_numpy

# access latest file if underneath file name is blanked out
output_data_directory = '../Output_data/'
files = sorted(os.listdir(output_data_directory))
filename = files[-1]
# filename = 
angles = read_file(output_data_directory +filename)
angles = convert_read_numpy(angles)

# Extract data
t = angles['time']
accx = angles['ax']
accy = angles['ay']
accz = angles['az']
gx = angles['gx']
gy = angles['gy']
gz = angles['gz']
angle1 = angles['be']
position = angles['pos']

# setup figure
fig, ax = plt.subplots(
    2, 2, figsize=(
        8, 6), sharex=True)

# use this to format graphs, keeps everything looking the same
ax = format_graph(ax)

# editing top left plot
plt.sca(ax[0])
plt.title('Plot of angle against seat position')
plt.plot(t, position, label='Position of Nao')
plt.ylabel('Named position')

# editing bottom left plot
plt.sca(ax[2])
plt.plot(t, angle1, label='Big Encoder')
plt.xlabel('Time (s)')
plt.ylabel('Angle (' + r'$^o)$')
plt.grid()

plt.legend(loc='upper left')

# upper right plot
plt.sca(ax[1])
plt.title('Plot of accelerometer values')
plt.plot(t, accx, label='Acceleration x')
plt.plot(t, accy, label='Acceleration y')
plt.plot(t, accz, label='Acceleration z')
plt.legend(loc='lower left')

# lower right plot
plt.sca(ax[3])
plt.title('Plot of gyrometer values')
plt.plot(t, gx, label='Gyro x')
plt.plot(t, gy, label='Gyro y')
plt.plot(t, gz, label='Gyro z')
plt.legend(loc='best')

plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig(
    'Figures/AnglePlot{}.eps'.format(filename.replace(" ", "")), format='eps')
