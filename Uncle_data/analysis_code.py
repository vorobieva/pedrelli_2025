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

#load data example
f=pathWD+'Raw_data_mutants_2-4M.xlsx'
V12P_3_1 = pd.read_excel(open(f, 'rb'), header=1, sheet_name="B3", index_col=0)
#Rename columns
cols_list = V12P_25_1.columns.tolist()
new_cols = []
for col in cols_list:
  val=col.split(',')[0]
  new_cols.append(float(val[6:]))
V12P_25_1.columns = new_cols
V12P_25_1 = V12P_25_1.drop(["Wavelength"])
V12P_25_1 = V12P_25_1.dropna()

# With cooperaiviyt factor
fitfunc = lambda p, x: p[1] + (p[0] - p[1]) / (1 + np.exp(p[2]*(x - p[3])))
errfunc = lambda p, x, y: fitfunc(p, x) - y
p0 = [0.8, 1.0, 0.5, 85.0]
temp = np.linspace(70.0, 95.0, 50)

#Average fluorescence intensity around 330 and 350nm
dV12P_3_1 = ((V12P_3_1.iloc[212]+V12P_3_1.iloc[211]+V12P_3_1.iloc[210]+V12P_3_1.iloc[209]+V12P_3_1.iloc[213]+V12P_3_1.iloc[214]+V12P_3_1.iloc[215])/7)/((V12P_3_1.iloc[170]+V12P_3_1.iloc[169]+V12P_3_1.iloc[168]+V12P_3_1.iloc[167]+V12P_3_1.iloc[171]+V12P_3_1.iloc[172]+V12P_3_1.iloc[173])/7)

#Average two replicates
dV12P_3 = (dV12P_3_1.to_frame().reset_index() + dV12P_3_2.to_frame().reset_index())/2

dV12P_3.columns = ['V12P_temp', 'V12P_ratio']

#Plot the change in fluorescence ratio. Also fit a sigmoidal unforlding transition to the data.
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4,7))
fig.tight_layout()
dV12P_3.plot(x='V12P_temp', y='V12P_ratio', ax=axes[2,1], color='grey', marker='', markersize=5, label='V12P')
p5_A, success = optimize.leastsq(errfunc, p0[:], args=(dV12P_3['V12P_temp'], dV12P_3['V12P_ratio']))
axes[2,1].plot(temp, fitfunc(p5_A, temp), "black", linewidth=0.75, linestyle='dashed')

#print the Tm extracted from the sigmoidal fit (p5_A[3]) as well as the cooperativity factor (p5_A[2])
print("Tm V12P: " + str(p5_A[3]))
print("c V12P : " + str(p5_A[2]))
#add a vertical line to the plot to mark the Tm
axes[2,1].vlines(x=87.48647732892208, ymin=0.868, ymax=0.89, colors='grey',linestyles='dashed', linewidth=0.5)
