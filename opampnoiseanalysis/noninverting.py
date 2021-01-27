#!/usr/bin/env python3
""" Inverting Operational Amplifier Noise Calculation

Takes into account all the noise sources in an inverting topology.

Author: Douglass Murray

"""
import os
import numpy as np
import matplotlib.pyplot as plt

def noninvertingTopoImageDisplay():
    os.system("open ../images/noninverting.png")  # Will open in Preview.

def resistorNoise(resistor, temp=None):
    """Calculates Johnson–Nyquist noise (thermal noise) of resistors.

    Args:
        resistor: Resistor value (Ohm)
        temp: Temperature of resistor, default 20 C
    
    Returns:
        resistorVoltageNoise: thermal voltage noise of resistor
    """
    # Resistors Johnson thermal noise
    temp = 20 if temp is None else temp # set temp at room temp as default
    k = 1.38e-23  # J/K, Boltzmann's constant
    resistorVoltageNoise = np.sqrt(4 * k * (temp + 273) * resistor)  # V/sqrt(Hz)
    return resistorVoltageNoise


gain = Rfeedback / Rin

# RTI Total Noise (V/sqrt(Hz))
def noninvertingRTINoise(Rsource, rOne, rTwo, rThree, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtOneHz, inoiseAtHighHz, atFreq=None, iNoiseAtOpAmpFreq=None, temp=None):
    """Calculates RTI noise of inverting op-amp topology.

    Args:
        Rsource: Source resistance
        rOne: Input resistor
        rTwo: Feedback resistor 
        rThree: Noninverted input resistor (which is usally tied to GND)
        vnoiseAtOneHz: op-amp voltage noise at low freq (based on datasheet)
        vnoiseAtHighHz: op-amp voltage noise at high freq (based on datasheet)
        inoiseAtOneHz: op-amp current noise at low freq (based on datasheet)
        inoiseAtHighHz: op-amp current noise at high freq (based on datasheet)
        atFreq: user specified frequency
        iNoiseAtOpAmpFreq: (specific to JFET-input type op-amps) current noise increase with freq (based on datasheet), default=0
        temp: temperature in C of resistors, default 20 (room temp)
    
    Returns:
        RTINoise: total RTI noise
    """
    atFreq = 1000 if atFreq is None else atFreq # set atFreq to 1 kHz as default
    iNoiseAtOpAmpFreq = 0 if iNoiseAtOpAmpFreq is None else iNoiseAtOpAmpFreq # set iNoiseAtOpAmpFreq to 0 as default
    temp = 20 if temp is None else temp  # set temp to room temp as default
    gain = rTwo / rOne
    # Op-amp specific parameters based on datasheet
    ampVoltNoise = opampVNoiseAtFreq(vnoiseAtOneHz, vnoiseAtHighHz, atFreq)
    ampCurrentNoise = opampINoiseAtFreq(inoiseAtOneHz, inoiseAtHighHz, atFreq, iNoiseAtOpAmpFreq)


