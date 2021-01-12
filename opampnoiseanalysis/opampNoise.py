#!/usr/bin/env python3
""" Intrinsic Operational Amplifier Noise Calculation

Plots voltage and current noise of operational amplifier.

Author: Douglass Murray

"""
import numpy as np
import matplotlib.pyplot as plt

# TODO: have these imported from another script
opampVNoiseDensityLowFreq = 6.5e-9 # V/sqrt(Hz)
opampVNoiseDensityHighFreq = 3.0e-9 # V/sqrt(Hz)
opampINoiseDensityLowFreq = 400e-15 # A/sqrt(Hz)
opampINoiseDensityHighFreq = 6300e-15 # A/sqrt(Hz)
opampINoiseDensityAtFreq = 0 # Hz

freqs = np.array([1, 2, 5, 10, 22, 46, 100, 215, 463, 1000, 2150, 4630, 10000, 21500, 46300, 100000, 215000, 463000, 1000000])

VNoiseAtFreq = np.array([])
for i, element in enumerate(freqs):
    VNoiseAtFreq = np.append(VNoiseAtFreq, (np.sqrt(np.square(opampVNoiseDensityHighFreq) + np.square(opampVNoiseDensityLowFreq) / element)))
print(VNoiseAtFreq)

INoiseAtFreq = np.array([])
if opampINoiseDensityAtFreq == 0:
    for i, element in enumerate(freqs):
        INoiseAtFreq = np.append(INoiseAtFreq, np.sqrt(np.square(opampINoiseDensityLowFreq) + np.square(opampINoiseDensityHighFreq) / element))
else:
    for i, element in enumerate(freqs):
        INoiseAtFreq = np.append(INoiseAtFreq, np.sqrt(np.square(opampINoiseDensityLowFreq) + np.square(opampINoiseDensityHighFreq) * np.square(element) / np.square(opampINoiseDensityAtFreq)))
print(INoiseAtFreq)

plt.loglog(freqs, VNoiseAtFreq, label="Vnoise")
plt.loglog(freqs, INoiseAtFreq, label="Inoise")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/sqrt(Hz)) or (A/sqrt(Hz))")
plt.title("Spectral Noise Density")
plt.grid(True, which="minor")
plt.legend()
plt.show()
