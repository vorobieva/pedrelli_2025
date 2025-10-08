import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import struct
import os
import glob
import seaborn as sns
import pyabf
from scipy import signal

#define the necessary functions
def detrend_signal(time, data, poly_order=3, plot=True):
    """Remove polynomial trend from a signal."""
    coeffs = np.polyfit(time, data, poly_order)
    trend = np.polyval(coeffs, time)
    detrended = data - trend

    if plot:
        fig, axes = plt.subplots(2, 1, figsize=(8, 6))
        axes[0].plot(time, data)
        axes[0].set(title="Original Signal", xlabel="Time", ylabel="Current")

        axes[1].plot(time, detrended)
        axes[1].set(title="Detrended Signal", xlabel="Time", ylabel="Current")

        plt.tight_layout()
        plt.figure(figsize=(6, 4))
        plt.plot(time, trend, "r--", linewidth=2)
        plt.title("Detrending Polynomial")
        plt.xlabel("Time")
        plt.ylabel("Trend")

    return detrended, trend


def downsample_signal(time, data, target_fs, orig_fs=None):
    """Downsample signal to target sampling rate (Hz) with anti-alias filtering."""
    if orig_fs is None:
        # estimate sampling frequency from time vector
        dt = np.median(np.diff(time))
        orig_fs = 1.0 / dt
        print(orig_fs)

    # compute integer downsampling factor
    decimation_factor = int(round(orig_fs / target_fs))
    if not np.isclose(orig_fs / decimation_factor, target_fs, rtol=1e-3):
        raise ValueError("Target fs must be integer divisor of original fs.")

    # decimate with built-in anti-alias filter
    data_ds = signal.decimate(data, decimation_factor, ftype="iir", zero_phase=True)
    time_ds = time[::decimation_factor]

    return time_ds, data_ds, target_fs


def bessel_filter(order, cutoff_hz, fs):
    """Design a digital low-pass Bessel filter using bilinear transform."""
    z, p, k = signal.bessel(order, 2 * np.pi * cutoff_hz, analog=True, output="zpk")
    num, den = signal.zpk2tf(z, p, k)
    numd, dend = signal.bilinear(num, den, fs)  # convert to digital filter
    return numd, dend


def apply_filter(data, order=8, cutoff_hz=40, fs=1000):
    """Zero-phase filter application (like MATLAB filtfilt)."""
    numd, dend = bessel_filter(order, cutoff_hz, fs)
    return signal.filtfilt(numd, dend, data)


def plot_filtered(time, raw, filtered, t_ds, raw_ds):
    """Compare raw and filtered signals."""
    fig, axes = plt.subplots(3, 1, figsize=(8, 9))
    axes[0].plot(time, raw)
    axes[0].set(title="Downsampled Raw Signal", xlabel="Time (s)", ylabel="Amplitude")

    axes[1].plot(time, filtered)
    axes[1].set(title="Filtered Signal (Bessel)", xlabel="Time (s)", ylabel="Amplitude")

    axes[2].plot(t_ds, raw_ds)
    axes[2].set(title="Downsampled Filtered Signal", xlabel="Time (s)", ylabel="Amplitude")

    plt.tight_layout()
    plt.show()

#create a list of all experiments to analyze (here in .abf format)
databf=[]
for i in range(0,80):
  #print(pathWD+exp[i]+"/*.abf")
  dat=glob.glob(pathWD+exp[i]+"/*.abf")
  print(dat)
  databf+=dat
print(databf)
print(len(databf))

#process the current data (change the code to focus on the relevant part of your data)
current=abf0.sweepY[0:800000]
t0=abf0.sweepX[0:800000]
cutoff_hz=2*np.pi*100
orig_fs=10000
# 1. Filter at original rate
filtered = apply_filter(current, order=8,cutoff_hz=cutoff_hz, fs=orig_fs)
t_ds, raw_ds, fs = downsample_signal(t0, filtered, target_fs=100,orig_fs=orig_fs)#
plot_filtered(t0, current, filtered, t_ds, raw_ds)

#plot the current intensity distribution as a diagram
abf0_pruned_pos=filtered
histogram = sns.histplot(abf0_pruned_pos, bins=50, stat='density')
density_curve = sns.kdeplot(abf0_pruned_pos, linewidth=1.5, color='black')
plt.show()
