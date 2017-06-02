#!/usr/bin/python

from util_planck import *
from colormath.color_objects import XYZColor, sRGBColor, xyYColor, HSVColor
from colormath.color_conversions import convert_color 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

#-- Params
num_colors = 10
num_illum = 5

colors = calc_planck_locus_single_poly(num_colors)
colors = colors

mypatches = []
rgb_values = []

for idx_illum,k in enumerate(range(1,num_illum)):
    for idx_col,c in enumerate(colors):
        #-- calculate rgb-values from xyY representation
        xyY = xyYColor(c[0], c[1], k/float(num_illum))
        rgb = convert_color(xyY, sRGBColor)
        rgb_np = np.array([rgb.rgb_r, rgb.rgb_g, rgb.rgb_b])

        #-- clip to [0,1]
        for j in range(3):
            rgb_np[j] = max(0,rgb_np[j])
            rgb_np[j] = min(1,rgb_np[j])

        rgb_values.append([rgb_np[0], rgb_np[1], rgb_np[2]])
        
        #-- only for plotting
        mypatches.append(patches.Rectangle( (idx_col,idx_illum), 1, 1, facecolor=rgb_np) )

#-- print rgb list for further re-use
print "colors = ["
for rgbv in rgb_values:
    print "\t",rgbv,"," # this way the output can directly be copied to other scripts
print "]"
#-- this is only for plotting
fig,ax = plt.subplots()
plt.title("Planckian Blackbody colors")

for p in mypatches:
    ax.add_patch(p)

ax.set_xlim((0,num_colors))
ax.set_ylim((0,num_illum-1)) # we started at 1

ax.set_xticks([])
ax.set_yticks([])

ax.set_xlabel("Temperature")
ax.set_ylabel("Illumination strength")


plt.show()
