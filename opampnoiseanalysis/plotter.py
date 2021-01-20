#!/usr/bin/env python3
""" Noise Plotting tool

Plots various noise calculations.

Author: Douglass Murray

"""
import os
import numpy as np
import matplotlib.pyplot as plt
from opampnoiseanalysis.opampnoise import *

def genericOpAmpNoisePlot(freqs, vNoise, iNoise):
    plt.figure()
    plt.subplot(211)
    plt.loglog(freqs, vNoise, label="voltage noise")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Noise (V/sqrt(Hz))")
    plt.title("Voltage Spectral Noise Density")
    plt.grid(True, which="minor")
    
    plt.subplot(212)
    plt.loglog(freqs, iNoise, label="current noise")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Noise (A/sqrt(Hz))")
    plt.title("Current Spectral Noise Density")
    plt.grid(True, which="minor")

    plt.subplots_adjust(hspace=0.6)
    plt.show()


def invertingNoisePlot(Rsource, rOne, rTwo, vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, iNoiseAtHz=None):
    iNoiseAtHz = 0 if iNoiseAtHz is None else iNoiseAtHz  # set iNoiseAtHz to 0 as default
    freq, vNoise, iNoise = opAmpNoise(vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, iNoiseAtHz)

    # Rsource noise per freq
    RsourceNoisePerFreq = Rsource * iNoise
    
    # Rsource + R1 || R2 noise per freq
    RcomboNoisePerFreq = iNoise * (Rsource + rOne) * rTwo / (Rsource + rOne + rTwo)
    totalResistorsNoise = np.sqrt(np.square(RsourceNoisePerFreq) + np.square(RcomboNoisePerFreq))
    totalinvertingNoisePerFreq = np.sqrt(np.square(iNoise) + np.square(totalResistorsNoise) + np.square(RsourceNoisePerFreq))

    plt.loglog(freq, totalinvertingNoisePerFreq, label="total noise")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Noise (V/sqrt(Hz))")
    plt.title("Voltage Spectral Noise Density")
    plt.grid(True, which="minor")
    plt.show()
