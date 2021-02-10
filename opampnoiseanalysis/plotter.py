#!/usr/bin/env python3
""" Noise Plotting tool

Plots various noise calculations.

Author: Douglass Murray

"""
import numpy as np
import matplotlib.pyplot as plt
from opampnoiseanalysis.opampnoise import *


def generic_opamp_noise_plot(freqs, vnoise, inoise):
    """Plots spectral voltage noise density of op-amp.

    Args:
        freqs: frequencies to plot along (x-axis)
        vnoise: voltage noise per frequency
        inoise: current noise per frequency
    """
    plt.figure()
    plt.subplot(211)
    plt.loglog(freqs, vnoise, label="voltage noise")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Noise (V/sqrt(Hz))")
    plt.title("Voltage Spectral Noise Density")
    plt.grid(True, which="minor")
    plt.subplot(212)
    plt.loglog(freqs, inoise, label="current noise")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Noise (A/sqrt(Hz))")
    plt.title("Current Spectral Noise Density")
    plt.grid(True, which="minor")

    plt.subplots_adjust(hspace=0.6)
    plt.show()


def invertingNoisePlot(r_source, r_one, r_two, vnoise_low_hz, vnoise_high_hz,
                       inoise_low_hz, inoise_high_hz, inoise_at_hz=None):
    """Plots spectral voltage noise density of inverting topology.

    Args:
        r_source: Source resistance
        r_one: Input resistor
        r_two: Feedback resistor
        vnoise_low_hz: op-amp voltage noise at low freq (based on datasheet)
        vnoise_high_hz: op-amp voltage noise at high freq (based on datasheet)
        inoise_low_hz: op-amp current noise at low freq (based on datasheet)
        inoise_high_hz: op-amp current noise at high freq (based on datasheet)
        inoise_at_hz: frequency which op-amp current noise was take (based on
        datasheet), default=0
    """
    # set inoise_at_hz to 0 as default
    inoise_at_hz = 0 if inoise_at_hz is None else inoise_at_hz
    freq, vnoise, inoise = opamp_noise(vnoise_low_hz, vnoise_high_hz,
                                       inoise_low_hz, inoise_high_hz,
                                       inoise_at_hz)

    # r_source noise per freq
    r_source_noise_per_freq = r_source * inoise

    # r_source + R1 || R2 noise per freq
    r_combo_noise_per_freq = (inoise * (r_source + r_one) * r_two
                              / (r_source + r_one + r_two))
    total_resistors_noise = np.sqrt(np.square(r_source_noise_per_freq)
                                    + np.square(r_combo_noise_per_freq))
    total_inverting_noise_per_freq = np.sqrt(np.square(inoise)
                                             + np.square(total_resistors_noise)
                                             + np.square(r_source_noise_per_freq))

    plt.loglog(freq, total_inverting_noise_per_freq, label="total noise")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Noise (V/sqrt(Hz))")
    plt.title("Voltage Spectral Noise Density")
    plt.grid(True, which="minor")
    plt.show()
