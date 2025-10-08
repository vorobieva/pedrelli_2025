import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import struct
import os
import glob
from scipy.optimize import curve_fit
from numpy import pi, r_
from scipy import optimize
import nmrglue as ng

##First plot 2D NMR data
# read data
dic, data = ng.bruker.read_pdata("/content/google_drive/MyDrive/data_analysis/NMR/20250522_Giacomo_V12T/2/pdata/1")

# read in axis ppm parameters
udic = ng.bruker.guess_udic(dic, data, strip_fake=True)
uc = {i: ng.fileiobase.uc_from_udic(udic, dim=i) for i in (0, 1)}
axis_limits = [*uc[1].ppm_limits(), *uc[0].ppm_limits()]

# contour levels
levels = [data.max() / 120 * 1.6**i for i in range(5)]  # change as needed

# plot
fig, ax = plt.subplots(figsize=(3.5, 2.5))

ax.contour(
    data.real,
    levels=levels,
    extent=axis_limits,
    cmap=plt.cm.Greys_r, # change as per your preference
    linewidths=1, # change as per your preference
)

ax.set_xlim(11, 6)  # change as needed
ax.set_ylim(130.5, 106.3)  # change as needed
ax.set_xlabel('1H (ppm)', fontsize='12')
ax.set_ylabel('15N (ppm)', fontsize='12')
ax.tick_params(labelsize='12')

##Second plot 1D NMR data
f0=pathWD+'20250424_Giacomo_1.txt'
f1=pathWD+'20250424_Giacomo_2.txt'
f2=pathWD+'20250424_Giacomo_3.txt'
f3=pathWD+'20250424_Giacomo_4.txt'
f4=pathWD+'20250424_Giacomo_5.txt'
f5=pathWD+'20250424_Giacomo_6.txt'

ind = np.linspace(12.71261978149414, -3.3126206131369926, num=32768)
ind = list(ind)

df0_nmr = pd.read_csv(f0, header=0, sep='\t+',skiprows=9, names=['1H'],engine='python')
df1_nmr = pd.read_csv(f1, header=0, sep='\t+',skiprows=9, names=['1H'],engine='python')
df2_nmr = pd.read_csv(f2, header=0, sep='\t+',skiprows=9, names=['1H'],engine='python')
df3_nmr = pd.read_csv(f3, header=0, sep='\t+',skiprows=9, names=['1H'],engine='python')
df4_nmr = pd.read_csv(f4, header=0, sep='\t+',skiprows=9, names=['1H'],engine='python')
df5_nmr = pd.read_csv(f5, header=0, sep='\t+',skiprows=9, names=['1H'],engine='python')

df0_nmr.index = ind
df1_nmr.index = ind
df2_nmr.index = ind
df3_nmr.index = ind
df4_nmr.index = ind
df5_nmr.index = ind

#sns.set_style(\"whitegrid\")
fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(2.5,7.5))
fig.tight_layout()

df0_nmr['1H'].plot(ax=axes[0],color='purple',linewidth=0.25)
df1_nmr['1H'].plot(ax=axes[1],color='silver',linewidth=0.25)
df2_nmr['1H'].plot(ax=axes[2],color='silver',linewidth=0.25)
df3_nmr['1H'].plot(ax=axes[3],color='silver',linewidth=0.25)
df4_nmr['1H'].plot(ax=axes[4],color='silver',linewidth=0.25)
df5_nmr['1H'].plot(ax=axes[5],color='silver',linewidth=0.25)

axes[0].set_xlim([11, 7.5])
axes[1].set_xlim([11, 7.5])
axes[2].set_xlim([11, 7.5])
axes[3].set_xlim([11, 7.5])
axes[4].set_xlim([11, 7.5])
axes[5].set_xlim([11, 7.5])


axes[0].set_ylim([22500.0, 57500])
axes[1].set_ylim([-15000.0, 25000])
axes[2].set_ylim([-15000.0, 25000])
axes[3].set_ylim([-15000.0, 25000])
axes[4].set_ylim([-15000.0, 25000])
axes[5].set_ylim([-15000.0, 25000])
plt.show()
