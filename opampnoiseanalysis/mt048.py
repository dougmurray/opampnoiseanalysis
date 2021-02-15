#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

freqs = np.arange(0.1, 1e6)
noise_corner_freq = 15
opamp_noise = 0.9e-9
high_freq_interest = 700000
low_freq_interest = 1000

# op-amp spectral noise density (V/sqrt(Hz))
pink_freq_range = freqs[freqs < noise_corner_freq]
white_freq_range = freqs[freqs > noise_corner_freq]
pink_noise_spectral_density = opamp_noise * np.sqrt(noise_corner_freq) * np.sqrt(1 / pink_freq_range)
white_noise_spectral_density = np.full_like(white_freq_range, opamp_noise)
opamp_total_noise_spectral_density = np.concatenate((pink_noise_spectral_density, white_noise_spectral_density), axis=None)  # V/sqrt(Hz)
print("Total Spectral Noise Density (V/sqrt(Hz)): ", opamp_total_noise_spectral_density)

# RMS noise (Vrms)
rms_noise_low_freq = opamp_noise * np.sqrt(noise_corner_freq * np.log(noise_corner_freq / low_freq_interest))
rms_noise_high_freq = opamp_noise * np.sqrt(high_freq_interest - noise_corner_freq)
# rms_total_noise = opamp_noise * np.sqrt((noise_corner_freq * np.log(noise_corner_freq / low_freq_interest)) + (high_freq_interest - noise_corner_freq))
rms_total_noise = np.sqrt(np.square(rms_noise_low_freq) + np.square(rms_noise_high_freq))
print("From %f to %f Hz bandwidth" % (low_freq_interest, high_freq_interest))
print("Total RMS Noise (Vrms): ", rms_total_noise)

# Peak-to-peak noise (V)
noise_p_p = 6.6 * rms_total_noise
print("Noise peak-to-peak (V_p_p): ", noise_p_p)

plt.loglog(freqs, opamp_total_noise_spectral_density)
plt.title("Voltage Noise Spectral Density")
plt.grid(True, which="minor")
plt.xlabel("Frequnecy (Hz)")
plt.ylabel("Noise (V/sqrt(Hz))")
plt.show()
