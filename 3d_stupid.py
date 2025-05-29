#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Use the provided data points with name as key and tuple of (IQ, Good/Evil, Having a Good Time) as value
data_points = {
    ".  Hegseth":      (80,   9, 1),  # (IQ, Good/Evil, Having a Good Time)
    ".  Adams":        (90,  -5, 2),
    ".  Trump":        (100, 10, 10),
    ".  MTG":          (80, 10, 11),
    ".  Noem":         (80, 7, 5),
    ".  Rubio":        (105, 5, 1),
    ".  Musk":         (110,  8, 3),
    ".  Duffy":        (95,  1, 8),
    ".  RFK":          (90,  5, 6),
    ".  Putin":        (125,  10, 12),
    ".  Vance":        (108,  6, 4),
    ".  Netanyahu":    (130,  8, 2),
    ".  Patel":        (95,  6, 7),
    ".  Bongino":      (90,  8, 1),
    ".  Mike Johnson": (100,  3, 3),
    ".  Ramaswamy":    (105,  1, 8),
    ".  Navaro":       (95,  4, 6),
}

# Create the 3D figure
#fig = plt.figure(figsize=(12, 10))
fig = plt.figure(figsize=(20, 14))
ax = fig.add_subplot(111, projection='3d')

# Generate a color map for better visual differentiation
cm = plt.cm.get_cmap('tab20')
colors = [cm(i/len(data_points)) for i in range(len(data_points))]

# Plot each person
for i, (name, (iq, good_evil, having_fun)) in enumerate(data_points.items()):
    # Extract the name without the leading dot and spaces
    clean_name = name.strip(". ")
    
    # Plot the scatter point
    ax.scatter(iq, good_evil, having_fun, 
               c=[colors[i]], marker='o', s=100)
    
    # Add text label next to each point
    #ax.text(iq, good_evil, having_fun, f'{clean_name}', fontsize=8)
    ax.text(iq, good_evil, having_fun, f'{name}', fontsize=8)
    
    # Add a red line from the point down to the x-plane (IQ axis)
    ax.plot([iq, iq], [good_evil, good_evil], [having_fun, 0], 
            color='red', linestyle='--', linewidth=1.5, alpha=0.7)

# Set labels for axes
ax.set_xlabel('IQ')
ax.set_ylabel('Good/Evil')
ax.set_zlabel('Having a Good Time')

# Set axis limits with some padding
ax.set_xlim(70, 140)
ax.set_ylim(-10, 15)
ax.set_zlim(0, 15)

# Add title
ax.set_title('3D Personality Plot: IQ vs. Good/Evil vs. Having a Good Time', fontsize=14)

# Add a custom legend
legend_elements = []
for i, name in enumerate([name.strip(". ") for name in data_points.keys()]):
    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                          label=name, markerfacecolor=colors[i], markersize=8))

# Position the legend outside the plot
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1), 
          fontsize=8, title='People')

# Add grid lines for better depth perception
ax.grid(True)

# Print the data in the console as well
print("Person Data:")
for name, (iq, good_evil, having_fun) in data_points.items():
    clean_name = name.strip(". ")
    print(f"{clean_name}: IQ = {iq}, Good/Evil = {good_evil}, Having a Good Time = {having_fun}")

# Show the plot (this will make it interactive and rotatable with the mouse)
plt.tight_layout()
plt.show()
