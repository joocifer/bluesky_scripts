#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Use the provided data points with name as key and tuple of 
# (IQ, Good/Evil, Having a Good Time, Drug Use) as value
data_points = {
    ".  Hegseth":      (80,   9,  1, 10),    # (IQ, Good/Evil, Having a Good Time, Drug Use)
    ".  Adams":        (90,  -5,  2, 3),
    ".  Trump":        (100, 10, 10, 2),
    ".  MTG":          (80, 10, 11, 5),
    ".  Noem":         (80,  7,  5, 2),       # 0 drug use = pure blue
    ".  Rubio":        (105, 5,   1, 1),
    ".  Musk":         (110, 8,   3, 10),
    ".  Duffy":        (95,  1,   8, 3),
    ".  RFK":          (90,  5,   6, 6),
    ".  Putin":        (125, 10, 12, 2),      # 10 drug use = pure red
    ".  Vance":        (108, 6,   4, 4),
    ".  Netanyahu":    (130, 8,   2, 3),
    ".  Patel":        (95,  6,   7, 7),
    ".  Bongino":      (90,  8,   1, 7),
    ".  Mike Johnson": (100, 3,   3, 0),
    ".  Ramaswamy":    (105, 1,   8, 5),
    ".  Navaro":       (95,  4,   6, 6),
}

# Create the 3D figure
fig = plt.figure(figsize=(20, 14))
ax = fig.add_subplot(111, projection='3d')

# Plot each person with marker size and color based on drug use.
for name, (iq, good_evil, having_fun, drug_use) in data_points.items():
    # Remove the leading dot and spaces for display if needed.
    clean_name = name.strip(". ")
    
    # Compute a normalized value for drug use (0.0 to 1.0).
    drug_norm = drug_use / 10.0
    
    # Compute marker color: pure blue (0,0,1) if drug_use is 0, pure red (1,0,0) if drug_use is 10.
    marker_color = (drug_norm, 0, 1 - drug_norm)
    
    # Compute marker size to correlate with drug use.
    marker_size = 50 + drug_use * 10
    
    # Plot the scatter point.
    ax.scatter(iq, good_evil, having_fun, color=marker_color, marker='o', s=marker_size)
    
    # Add a text label next to the point.
    ax.text(iq, good_evil, having_fun, f'{name}', fontsize=8)
    
    # Draw a red dashed line from the point down to the x-y plane (z=0) for depth reference.
    ax.plot([iq, iq], [good_evil, good_evil], [having_fun, 0], 
            color='red', linestyle='--', linewidth=1.5, alpha=0.7)

# Set axis labels.
ax.set_xlabel('IQ')
ax.set_ylabel('Good/Evil')
ax.set_zlabel('Having a Good Time')

# Define axis limits with padding.
ax.set_xlim(70, 140)
ax.set_ylim(-10, 15)
ax.set_zlim(0, 15)

# Add the plot title with a note on the drug use representation.
ax.set_title('3D Personality Plot: IQ vs. Good/Evil vs. Having a Good Time\n'
             '(Marker color and size represent Drug Use)', fontsize=14)

# Create a mapping of clean names to original dictionary keys
name_mapping = {name.strip(". "): name for name in data_points.keys()}

# Create a sorted legend list based on drug use, highest at the top
legend_elements = sorted(
    [
        plt.Line2D([0], [0], marker='o', color='w', label=clean_name, 
                   markerfacecolor=(drug_use / 10.0, 0, 1 - (drug_use / 10.0)), markersize=8)
        for clean_name, name in name_mapping.items()
        for _, _, _, drug_use in [data_points[name]]  # Extract drug use from original name
    ],
    key=lambda elem: -data_points[name_mapping[elem.get_label()]][3]  # Sort by drug use descending
)

# Position the legend outside the main plot area.
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1), 
          fontsize=8, title='People (Sorted by Drug Use)')

# Enable grid lines to aid depth perception.
ax.grid(True)

# Print the data to the console including drug use.
print("Person Data:")
for name, (iq, good_evil, having_fun, drug_use) in data_points.items():
    clean_name = name.strip(". ")
    print(f"{clean_name}: IQ = {iq}, Good/Evil = {good_evil}, Having a Good Time = {having_fun}, Drug Use = {drug_use}")

# Optimize layout and display the interactive plot.
plt.tight_layout()
plt.show()
