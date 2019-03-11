import matplotlib.pyplot as plt
import numpy as np
from random import random
from graph_functions import format_graph

fig, ax = plt.subplots()
ax = format_graph(ax)

x = np.linspace(0, 5, 25)
# Created some random numbers and these illustrate the point quite well
y = [0.19372539709688008, 0.33938330167221986, 0.5221322433249442, 0.5993647654740099, 0.8864862580838297, 1.051816112961354, 1.0111515292848758, 1.008788983683322, 1.0135888624789915, 1.1163402016396407, 0.8849787982701526, 0.9409059816754168, 0.7459870990277785, 0.42613590899355486, 0.3776901660529006, 0.09220466195996868, -0.04659839718513614, -0.20153143593410894, -0.5279932799719772, -0.5469714783209003, -0.851256333861391, -0.8282102729634235, -0.8737824932779301, -0.8927337135446781, -0.8309776479201566]
ratio_x_y = 5 / (max(y) - min(y))
print ratio_x_y

def moving_average(values, window_size):
    ma = [np.sum(values[i:i+window_size])/window_size for i,
          _ in enumerate(values[:-window_size+1])]
    return ma

x_moving_average = x[2:-2]
y_moving_average = moving_average(y, 5) 
plt.plot(x, y, label='Angle data')
plt.plot(x[2:-2], y_moving_average, label='Moving average')
ax.set_facecolor('#eeeeee')

index_maxima = (np.diff(np.sign(np.diff(y))) < 0).nonzero()[0] + 1
smooth_maxima = (np.diff(np.sign(np.diff(y_moving_average))) < 0).nonzero()[0] + 1
x_fake_max = x[index_maxima[-2]]
x_calculated_max = x_moving_average[smooth_maxima[0]]

plt.xticks([])
plt.yticks([])
plt.text(x_fake_max / 5 + 1.2 / 5, 0.85, "Latest\nlocal maximum", horizontalalignment='center',
     verticalalignment='center',
     transform=ax.transAxes, size=16)
plt.text(x_calculated_max / 5, 0.35, "Calculated\nmaximum", horizontalalignment='center',
     verticalalignment='center',
     transform=ax.transAxes, size=16)

plt.arrow(x_fake_max + 1.0, y[index_maxima[-2]], -0.8, 0.0, length_includes_head=True, color='Black', width=0.01, head_width=0.05, head_length=0.1)
plt.arrow(x_calculated_max, 0, 0, 0.9, length_includes_head=True, color='Black', width=0.02, head_width=0.125, head_length=0.05)



plt.title('Comparison between large encoder values\nbefore and after moving average')
plt.ylabel('Angle')
plt.xlabel('Time')
plt.legend(loc='lower left')

fig.tight_layout()
plt.show()
fig.savefig('Figures/MovingAverageDiagram.eps', format='eps')