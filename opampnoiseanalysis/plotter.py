#!/usr/bin/env python3
""" Noise Plotting tool

Plots various noise calculations.

Author: Douglass Murray

"""
import os
import numpy as np
import matplotlib.pyplot as plt
# from opampnoiseanalysis.o   import opampnoise
from opampnoiseanalysis.opampnoise import *

def genericOpAmpNoisePlot(freqs, vNoise, iNoise):
    plt.figure()
    plt.subplot(211)
    plt.loglog(freqs, vNoise, label="voltage noise")
    plt.xlabel("Frequecny (Hz)")
    plt.ylabel("Noise (V/sqrt(Hz))")
    plt.title("Voltage Spectral Noise Density")
    plt.grid(True, which="minor")
    
    plt.subplot(212)
    plt.loglog(freqs, iNoise, label="current noise")
    plt.xlabel("Frequecny (Hz)")
    plt.ylabel("Noise (A/sqrt(Hz))")
    plt.title("Current Spectral Noise Density")
    plt.grid(True, which="minor")

    # plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
    plt.subplots_adjust(hspace=0.6)
    plt.show()
    
