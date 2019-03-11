import matplotlib.pyplot as plt
import numpy as np
from graph_functions import format_graph
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import matplotlib.patches as patches

fig, ax = plt.subplots(1, figsize=(12,8))
# ax = format_graph(ax)

l = 1
angle_before, angle_after = -10, 15
angle_before, angle_after = angle_before * np.pi/180, angle_after * np.pi/180

x_before, y_before = l * np.sin(angle_before), 2 - l * np.cos(angle_before)
x_after, y_after = l * np.sin(angle_after), 2 - l * np.cos(angle_after)

x_line1, y_line1 = [x_before, 0], [y_before, 2]
x_line2, y_line2 = [x_after, 0], [y_after, 2]

plt.sca(ax)
plt.plot(x_line1, y_line1, x_line2, y_line2)
plt.plot([0, 0], [2, 0], linestyle='--')
plt.xlim([-0.5, 1.5])
plt.ylim([0.7, 2.2])
plt.xticks([])
plt.yticks([])
plt.text(0.10, 0.17, r"$(\theta_1, t_1)$", horizontalalignment='center',
     verticalalignment='center',
     transform=ax.transAxes, size=24)
plt.text(0.42, 0.17, r"$(\theta_2, t_2)$", horizontalalignment='center',
     verticalalignment='center',
     transform=ax.transAxes, size=24)
plt.text(0.30, 0.08, r"$(0, t_c)$", horizontalalignment='center',
     verticalalignment='center',
     transform=ax.transAxes, size=24)

style="Simple,tail_width=0.5,head_width=4,head_length=8"
kw = dict(arrowstyle=style, color="k")
a3 = patches.FancyArrowPatch((x_before,y_before), (x_after,y_after),connectionstyle="arc3,rad=.44", **kw)
plt.gca().add_patch(a3)

ax2 = zoomed_inset_axes(ax, 22, loc=1)
plt.sca(ax2)


x1, x2, y1, y2 = -0.02, 0.02, 1.95, 2.01
ax2.set_xlim(x1, x2)
ax2.set_ylim(y1, y2)
ax2.set_facecolor('#eeeeee')
plt.sca(ax2)
plt.xticks(visible=False)
plt.yticks(visible=False)
plt.xticks([])
plt.yticks([])
plt.plot(x_line1, y_line1, x_line2, y_line2)
plt.plot([0, 0], [2, 1], linestyle='--')

plt.text(0.44, 0.4, r"$\theta_1$", horizontalalignment='center',
     verticalalignment='center',
     transform=ax2.transAxes, size=24)
plt.text(0.61, 0.4, r"$\theta_2$", horizontalalignment='center',
     verticalalignment='center',
     transform=ax2.transAxes, size=24)
mark_inset(ax, ax2, loc1=2, loc2=3, ec="0.5", fc="w")

fig.tight_layout()
plt.show()
fig.savefig('Figures/InterpolationDiagram.eps', format='eps')
