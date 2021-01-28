#!/usr/bin/env python3
""" Intrinsic Operational Amplifier Noise Calculation

Plots voltage and current noise of operational amplifier.

Author: Douglass Murray

"""
import numpy as np
import matplotlib.pyplot as plt

# TODO: have these imported from another script
opamp_vnoise_density_low_freq = 6.5e-9 # V/sqrt(Hz)
opamp_vnoise_density_high_freq = 3.0e-9 # V/sqrt(Hz)
opamp_inoise_density_low_freq = 400e-15 # A/sqrt(Hz)
opamp_inoise_density_high_freq = 6300e-15 # A/sqrt(Hz)
opamp_inoise_density_at_freq = 0 # Hz

freqs = np.array([1, 2, 5, 10, 22, 46, 100, 215, 463, 1000, 2150, 4630, 10000, 21500, 46300, 100000, 215000, 463000, 1000000])

vnoise_at_freq = np.array([])
for i, element in enumerate(freqs):
    vnoise_at_freq = np.append(vnoise_at_freq, (np.sqrt(np.square(opamp_vnoise_density_high_freq) + np.square(opamp_vnoise_density_low_freq) / element)))
print(vnoise_at_freq)

inoise_at_freq = np.array([])
if opamp_inoise_density_at_freq == 0:
    for i, element in enumerate(freqs):
        inoise_at_freq = np.append(inoise_at_freq, np.sqrt(np.square(opamp_inoise_density_low_freq) + np.square(opamp_inoise_density_high_freq) / element))
else:
    for i, element in enumerate(freqs):
        inoise_at_freq = np.append(inoise_at_freq, np.sqrt(np.square(opamp_inoise_density_low_freq) + np.square(opamp_inoise_density_high_freq) * np.square(element) / np.square(opamp_inoise_density_at_freq)))
print(inoise_at_freq)

plt.loglog(freqs, vnoise_at_freq, label="vnoise")
plt.loglog(freqs, inoise_at_freq, label="inoise")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/sqrt(Hz)) or (A/sqrt(Hz))")
plt.title("Intrinsic Op-amp Spectral Noise Density")
plt.grid(True, which="minor")
plt.legend()
plt.show()
