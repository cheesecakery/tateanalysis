# TO DO:
    # visualise change in mediums over time?

import json
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

# Opens file up
with open('stats.json') as file:
    stats = json.load(file)

x = list(stats)[-100:]

mediums = ['photography', 'painting', 'printing', 'drawing', 'sculpture']
# mediums = stats['2012']['mediums'].keys()
ys = {}
for medium in mediums:
    y = []
    for yr in x:
        y.append(stats[yr]["mediums"][medium])
    ys[medium] = y

plt.xlim(0, 100)

# Create a line chart
for medium in mediums:
    plt.plot(x, ys[medium], marker=None, linestyle='-', label=medium)

plt.xticks(rotation = 45, ticks=range(0, 100, 5))

plt.legend()

# Display grid
plt.grid(True)

# Show the plot
plt.show()