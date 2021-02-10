#!/usr/bin/env python3
""" Operational Amplifier Noise Model

Takes op-amp intrinsic properties as inputs and outputs voltage
and current noise over 1 - 1 MHz frequency range.

Author: Douglass Murray

"""
import numpy as np
import pandas as pd
from opampnoiseanalysis.plotter import *

# freq_range = np.array([1, 2, 5, 10, 22, 46, 100, 215, 463, 1000, 2150, 4630,
#                       10000, 21500, 46300, 100000, 215000, 463000, 1000000])
# opamp_vnoise = np.array([])
# opamp_inoise = np.array([])
# vnoise_low_hz = 50e-9  # V/sqrt(Hz)
# vnoise_high_hz = 8.0e-9  # V/sqrt(Hz)
# inoise_low_hz = 200e-12  # A/sqrt(Hz)
# inoise_high_hz = 1050e-12  # A/sqrt(Hz)
# inoise_at_hz = 0  # Hz
# uGBW = 1.0e6 # Hz


def opamp_noise(vnoise_low_hz, vnoise_high_hz, inoise_low_hz, inoise_high_hz,
                inoise_at_hz=None, amp_gain_bandwidth=None):
    """Op-amp intrinsic noise calculation.

    Args:
        vnoise_low_hz: op-amp voltage noise at low freq (based on datasheet)
        vnoise_high_hz: op-amp voltage noise at high freq (based on datasheet)
        inoise_low_hz: op-amp current noise at low freq (based on datasheet)
        inoise_high_hz: op-amp current noise at high freq (based on datasheet)
        inoise_at_hz: (specific to JFET-input type op-amps) current noise
                        increase with freq (based on datasheet), default=0

    Returns:
        freq_range: frequency range, 1 - 1 MHz (Hz)
        opamp_vnoise: op-amp voltage noise at frequencies in range (V/sqrt(Hz))
        opamp_inoise: op-amp current noise at frequencies in range (A/sqrt(Hz))
    """
    # set inoise_at_hz to 0 as default
    inoise_at_hz = 0 if inoise_at_hz is None else inoise_at_hz
    # set unity gain bandwidth to resonable default if not included
    amp_gain_bandwidth = 1e6 if amp_gain_bandwidth is None else amp_gain_bandwidth
    freq_range = np.array([1, 2, 5, 10, 22, 46, 100, 215, 463, 1000,
                          2150, 4630, 10000, 21500, 46300, 100000, 215000,
                          463000, 1000000])
    opamp_vnoise = np.array([])
    opamp_inoise = np.array([])
    for i, element in enumerate(freq_range):
        vnoise = np.sqrt(np.square(vnoise_high_hz) + np.square(vnoise_low_hz)
                         / element)
        opamp_vnoise = np.append(opamp_vnoise, vnoise)

    for i, element in enumerate(freq_range):
        if not inoise_at_hz:
            inoise = np.sqrt(np.square(inoise_low_hz)
                             + np.square(inoise_high_hz) / element)
            opamp_inoise = np.append(opamp_inoise, inoise)
        else:
            # This is a little off
            inoise = np.sqrt(np.square(inoise_low_hz)
                             + np.square(inoise_high_hz) * np.square(element)
                             / np.square(inoise_at_hz))
            opamp_inoise = np.append(opamp_inoise, inoise)

    return freq_range, opamp_vnoise, opamp_inoise


def opamp_vnoise_at_freq(vnoise_low_hz, vnoise_high_hz, at_freq=None):
    """Op-amp intrinsic voltage noise calculation at specified frequency.

    Args:
        at_freq: specified frequency, default=1000 (Hz)
        vnoise_low_hz: op-amp voltage noise at low freq (based on datasheet)
        vnoise_high_hz: op-amp voltage noise at high freq (based on datasheet)

    Returns:
        opamp_vnoise_at_freq: op-amp voltage noise
                              at specified frequency (V/sqrt(Hz))
    """
    # set at_freq to 1 kHz as default
    at_freq = 1000 if at_freq is None else at_freq
    opamp_vnoise_at_freq = np.sqrt(np.square(vnoise_high_hz)
                                   + np.square(vnoise_low_hz) / at_freq)
    return opamp_vnoise_at_freq


def opamp_inoise_at_freq(inoise_low_hz, inoise_high_hz, at_freq=None,
                         inoise_at_hz=None):
    """Op-amp intrinsic current noise calculation at specified frequency.

    Args:
        at_freq: specified frequency, default=1000 (Hz)
        inoise_low_hz: op-amp current noise at low freq (based on datasheet)
        inoise_high_hz: op-amp current noise at high freq (based on datasheet)
        inoise_at_hz: (specific to JFET-input type op-amps) current noise
                       increase with freq (based on datasheet), default=0

    Returns:
        opamp_inoise_at_freq: op-amp current noise
                              at specified frequency (A/sqrt(Hz))
    """
    # set at_freq to 1 kHz as default
    at_freq = 1000 if at_freq is None else at_freq
    inoise_at_hz = 0 if inoise_at_hz is None else inoise_at_hz
    if not inoise_at_hz:
        opamp_inoise_at_freq = np.sqrt(np.square(inoise_low_hz)
                                       + np.square(inoise_high_hz) / at_freq)
    else:
        opamp_inoise_at_freq = np.sqrt(np.square(inoise_low_hz) + np.square(
            inoise_high_hz) + np.square(element) / np.square(inoise_at_hz))
    return opamp_inoise_at_freq


def opamp_choose_input():
    """Helper function for user to choose between inputing discrete vlaues
       or import via csv file.

    Args:
        None

    Returns:
        vnoise_low_hz: op-amp voltage noise at low freq (based on datasheet)
        vnoise_high_hz: op-amp voltage noise at high freq (based on datasheet)
        inoise_low_hz: op-amp current noise at low freq (based on datasheet)
        inoise_high_hz: op-amp current noise at high freq (based on datasheet)
        inoise_at_hz: (specific to JFET-input type op-amps) current noise
                       increase with freq (based on datasheet), default=0
        amp_gain_bandwidth: op-amp unity gain bandwidth
    """
    opamp_choice = int(input("Input (1) op-amp values or (2) pick op-amp: "))
    if opamp_choice == 1:
        # direct input of op-amp values
        vnoise_low_hz = float(input("vnoise @ 1 Hz: "))
        vnoise_high_hz = float(input("vnoise @ 10 MHz: "))
        inoise_low_hz = float(input("inoise @ 1 Hz: "))
        inoise_high_hz = float(input("inoise @ 10 MHz: "))
        inoise_at_hz = float(input("inoise Freq (default = 0): "))
        amp_gain_bandwidth = float(input("Input op-amp unity gain BW (Hz): "))
    elif opamp_choice == 2:
        opamp_name = str(input("Input op-amp name: "))
        # Search and pick op-amp
        # csv format: Device, VnoiseLow, VnoiseHigh, InoiseLow,
        #              InoiseHigh, InoiseSpecFreq, UGBW
        opamps = pd.read_csv('./opampdata/opampData.csv')
        single_opamp = opamps.loc[opamps['Device'] == opamp_name]
        # if Pandas version is < version 0.24
        specific_opamp_values = single_opamp.values
        # if Pandas version is > version 0.24
        # specific_opamp_values = single_opamp.to_numpy(copy=True)
        vnoise_low_hz = specific_opamp_values[0, 1]
        vnoise_high_hz = specific_opamp_values[0, 2]
        inoise_low_hz = specific_opamp_values[0, 3]
        inoise_high_hz = specific_opamp_values[0, 4]
        inoise_at_hz = specific_opamp_values[0, 5]
        amp_gain_bandwidth = specific_opamp_values[0, 6]
    else:
        print("Please choose either (1) op-amp values or (2) pick op-amp.")

    return (vnoise_low_hz, vnoise_high_hz, inoise_low_hz, inoise_high_hz,
            inoise_at_hz, amp_gain_bandwidth)
