#!/usr/bin/env python3
""" Inverting Operational Amplifier Noise Calculation

Takes into account all the noise sources in an inverting topology.

Author: Douglass Murray

"""
import os
import numpy as np
import matplotlib.image as img
from opampnoiseanalysis.opamp_noise import *

def inverting_topo_image_display():
    """Displays inverting op-amp topology pic."""
    os.system("open images/inverting.png")  # Will open in Preview.

def resistor_noise(resistor, temp=None):
    """Calculates Johnson–Nyquist noise (thermal noise) of resistors.

    Args:
        resistor: Resistor value (Ohm)
        temp: Temperature of resistor, default 20 C
    
    Returns:
        resistor_vnoise: thermal voltage noise of resistor
    """
    # Resistors Johnson thermal noise
    temp = 20 if temp is None else temp # set temp at room temp as default
    k = 1.38e-23  # J/K, Boltzmann's constant
    resistor_vnoise = np.sqrt(4 * k * (temp + 273) * resistor)  # V/sqrt(Hz)
    return resistor_vnoise

# RTI Total Noise (V/sqrt(Hz))
def inverting_rti_noise(r_source, r_one, r_two, r_three, vnoise_low_hz, vnoise_high_hz, inoise_low_hz, inoise_high_hz, at_freq=None, inoise_at_hz=None, temp=None):
    """Calculates RTI noise of inverting op-amp topology.

    Args:
        r_source: Source resistance
        r_one: Input resistor
        r_two: Feedback resistor 
        r_three: Noninverted input resistor (which is usally tied to GND)
        vnoise_low_hz: op-amp voltage noise at low freq (based on datasheet)
        vnoise_high_hz: op-amp voltage noise at high freq (based on datasheet)
        inoise_low_hz: op-amp current noise at low freq (based on datasheet)
        inoise_high_hz: op-amp current noise at high freq (based on datasheet)
        at_freq: user specified frequency
        inoise_at_hz: (specific to JFET-input type op-amps) current noise increase with freq (based on datasheet), default=0
        temp: temperature in C of resistors, default 20 (room temp)
    
    Returns:
        rti_noise: total RTI noise
    """
    at_freq = 1000 if at_freq is None else at_freq # set at_freq to 1 kHz as default
    inoise_at_hz = 0 if inoise_at_hz is None else inoise_at_hz # set inoise_at_hz to 0 as default
    temp = 20 if temp is None else temp  # set temp to room temp as default
    gain = r_two / r_one
    # Op-amp specific parameters based on datasheet
    opamp_vnoise = opamp_vnoise_at_freq(vnoise_low_hz, vnoise_high_hz, at_freq)
    opamp_inoise = opamp_inoise_at_freq(inoise_low_hz, inoise_high_hz, at_freq, inoise_at_hz)

    # RTI Noise Contributions (V/sqrt(Hz))
    inverted_input_rti_noise = opamp_inoise * (r_source + r_one) * r_two / (r_source + r_one + r_two) # V/sqrt(Hz)
    noninverted_input_rti_noise = opamp_vnoise # V/sqrt(Hz), direct contribution in inverted topology
    r_three_noise = resistor_noise(r_three, temp) # V/sqrt(Hz)
    r_two_noise = resistor_noise(r_two, temp) / gain # V/sqrt(Hz)
    r_one_noise = resistor_noise(r_one, temp) # V/sqrt(Hz)
    r_source_noise = resistor_noise(r_source, temp) # V/sqrt(Hz)

    rti_noise = gain * np.sqrt(np.square(inverted_input_rti_noise) + np.square(noninverted_input_rti_noise) + np.square(r_three_noise) + np.square(r_two_noise) + np.square(r_one_noise) + np.square(r_source_noise)) # V/sqrt(Hz)
    return rti_noise

# Integrated Noise over frequency (Vrms)
def inverting_integrated_noise(r_source, r_one, r_two, r_three, low_freq_of_interest, high_freq_of_interest, amp_gain_bandwidth, vnoise_low_hz, vnoise_high_hz, inoise_low_hz, inoise_high_hz, at_freq=None, inoise_at_hz=None, temp=None):
    """Calculates integrated noise of inverting op-amp topology.

    Args:
        r_source: Source resistance
        r_one: Input resistor
        r_two: Feedback resistor 
        r_three: Noninverted input resistor (which is usally tied to GND)
        low_freq_of_interest: low frequency of user interest
        high_freq_of_interest: high frequency of user interest
        amp_gain_bandwidth: op-amp unity gain bandwidth (based on datasheet)
        vnoise_low_hz: op-amp voltage noise at low freq (based on datasheet)
        vnoise_high_hz: op-amp voltage noise at high freq (based on datasheet)
        inoise_low_hz: op-amp current noise at low freq (based on datasheet)
        inoise_high_hz: op-amp current noise at high freq (based on datasheet)
        at_freq: user specified frequency
        inoise_at_hz: (specific to JFET-input type op-amps) current noise increase with freq (based on datasheet), default=0
        temp: temperature in C of resistors, default 20 (room temp)
    
    Returns:
        max_noise_bandwidth: maximum noise bandwidth
        integrated_noise: integrated noise over user's frequency of interest
    """
    at_freq = 1000 if at_freq is None else at_freq  # set at_freq to 1 kHz as default
    inoise_at_hz = 0 if inoise_at_hz is None else inoise_at_hz # set inoise_at_hz to 0 as default
    temp = 20 if temp is None else temp # set temp to room temp as default
    gain = r_two / r_one
    max_noise_bandwidth = 1.57 * amp_gain_bandwidth / gain
    r_three_noise = resistor_noise(r_three, temp)  # V/sqrt(Hz)
    r_two_noise = resistor_noise(r_two, temp) / gain  # V/sqrt(Hz)
    r_one_noise = resistor_noise(r_one, temp)  # V/sqrt(Hz)
    r_source_noise = resistor_noise(r_source, temp)  # V/sqrt(Hz)
    # Op-amp specific parameters based on datasheet
    opamp_vnoise = opamp_vnoise_at_freq(vnoise_low_hz, vnoise_high_hz, at_freq)
    opamp_inoise = opamp_inoise_at_freq(inoise_low_hz, inoise_high_hz, at_freq, inoise_at_hz)
    
    if max_noise_bandwidth < high_freq_of_interest:
        r_source_integrated_noise = r_source_noise * np.sqrt(max_noise_bandwidth - low_freq_of_interest) # Vrms
        r_one_integrated_noise = r_one_noise * np.sqrt(max_noise_bandwidth - low_freq_of_interest) # Vrms
        r_two_integrated_noise = np.sqrt(max_noise_bandwidth - low_freq_of_interest) * r_two_noise / gain # Vrms
        r_three_integrated_noise = r_three_noise * np.sqrt(max_noise_bandwidth - low_freq_of_interest) # Vrms
    else:
        r_source_integrated_noise = r_source_noise * np.sqrt(high_freq_of_interest - low_freq_of_interest) # Vrms
        r_one_integrated_noise = r_one_noise * np.sqrt(high_freq_of_interest - low_freq_of_interest) # Vrms
        r_two_integrated_noise = np.sqrt(high_freq_of_interest - low_freq_of_interest) * r_two_noise / gain # Vrms
        r_three_integrated_noise = r_three_noise * np.sqrt(high_freq_of_interest - low_freq_of_interest) # Vrms
    
    noninverted_input_integrated_noise = opamp_vnoise # Vrms, direct contribution in inverted topology
    inverted_input_integrated_noise = opamp_inoise * r_one * r_two / (r_one + r_two) # Vrms
    
    integrated_noise = gain * np.sqrt(np.square(r_source_integrated_noise) + np.square(r_one_integrated_noise) + np.square(r_two_integrated_noise) + np.square(r_three_integrated_noise) + np.square(noninverted_input_integrated_noise) + np.square(inverted_input_integrated_noise))  # Vrms
    return max_noise_bandwidth, integrated_noise
