#!/usr/bin/env python3
""" Inverting Operational Amplifier Noise Calculation

Takes into account all the noise sources in an inverting topology.

Author: Douglass Murray

"""
import os
import numpy as np
import matplotlib.pyplot as plt

def noninverting_topo_image_display():
    os.system("open ../images/noninverting.png")  # Will open in Preview.

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

gain = Rfeedback / Rin

# RTI Total Noise (V/sqrt(Hz))
def noninvertingRTINoise(r_source, r_one, r_two, r_three, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtOneHz, inoiseAtHighHz, at_freq=None, iNoiseAtOpAmpFreq=None, temp=None):
    """Calculates RTI noise of inverting op-amp topology.

    Args:
        r_source: Source resistance
        r_one: Input resistor
        r_two: Feedback resistor 
        r_three: Noninverted input resistor (which is usally tied to GND)
        vnoiseAtOneHz: op-amp voltage noise at low freq (based on datasheet)
        vnoiseAtHighHz: op-amp voltage noise at high freq (based on datasheet)
        inoiseAtOneHz: op-amp current noise at low freq (based on datasheet)
        inoiseAtHighHz: op-amp current noise at high freq (based on datasheet)
        at_freq: user specified frequency
        iNoiseAtOpAmpFreq: (specific to JFET-input type op-amps) current noise increase with freq (based on datasheet), default=0
        temp: temperature in C of resistors, default 20 (room temp)
    
    Returns:
        rti_noise: total RTI noise
    """
    at_freq = 1000 if at_freq is None else at_freq # set at_freq to 1 kHz as default
    iNoiseAtOpAmpFreq = 0 if iNoiseAtOpAmpFreq is None else iNoiseAtOpAmpFreq # set iNoiseAtOpAmpFreq to 0 as default
    temp = 20 if temp is None else temp  # set temp to room temp as default
    gain = r_two / r_one
    # Op-amp specific parameters based on datasheet
    ampVoltNoise = opampVNoiseAtFreq(vnoiseAtOneHz, vnoiseAtHighHz, at_freq)
    ampCurrentNoise = opampINoiseAtFreq(inoiseAtOneHz, inoiseAtHighHz, at_freq, iNoiseAtOpAmpFreq)


