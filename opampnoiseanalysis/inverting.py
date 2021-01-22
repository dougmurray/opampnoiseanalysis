#!/usr/bin/env python3
""" Inverting Operational Amplifier Noise Calculation

Takes into account all the noise sources in an inverting topology.

Author: Douglass Murray

"""
import os
import numpy as np
import matplotlib.image as img
from opampnoiseanalysis.opampnoise import *

def invertingTopoImageDisplay():
    """Displays inverting op-amp topology pic."""
    os.system("open images/inverting.png")  # Will open in Preview.

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

# RTI Total Noise (V/sqrt(Hz))
def invertingRTINoise(Rsource, rOne, rTwo, rThree, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtOneHz, inoiseAtHighHz, atFreq=None, iNoiseAtOpAmpFreq=None):
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
    
    Returns:
        RTINoise: total RTI noise
    """
    atFreq = 1000 if atFreq is None else atFreq # set atFreq to 1 kHz as default
    iNoiseAtOpAmpFreq = 0 if iNoiseAtOpAmpFreq is None else iNoiseAtOpAmpFreq # set iNoiseAtOpAmpFreq to 0 as default
    gain = rTwo / rOne
    # Op-amp specific parameters based on datasheet
    ampVoltNoise = opampVNoiseAtFreq(vnoiseAtOneHz, vnoiseAtHighHz, atFreq)
    ampCurrentNoise = opampINoiseAtFreq(inoiseAtOneHz, inoiseAtHighHz, atFreq, iNoiseAtOpAmpFreq)

    # RTI Noise Contributions (V/sqrt(Hz))
    invertedInputRTINoise = ampCurrentNoise * (Rsource + rOne) * rTwo / (Rsource + rOne + rTwo) # V/sqrt(Hz)
    noninvertedInputRTINoise = ampVoltNoise # V/sqrt(Hz), direct contribution in inverted topology
    RnoninvertedNoise = resistorNoise(rThree) # V/sqrt(Hz)
    RfeedbackNoise = resistorNoise(rTwo) / gain # V/sqrt(Hz)
    RinNoise = resistorNoise(rOne) # V/sqrt(Hz)
    RsourceNoise = resistorNoise(Rsource) # V/sqrt(Hz)

    RTINoise = gain * np.sqrt(np.square(invertedInputRTINoise) + np.square(noninvertedInputRTINoise) + np.square(RnoninvertedNoise) + np.square(RfeedbackNoise) + np.square(RinNoise) + np.square(RsourceNoise)) # V/sqrt(Hz)
    return RTINoise

# Integrated Noise over frequency (Vrms)
def invertingIntegratedNoise(Rsource, rOne, rTwo, rThree, lowFreqOfInterest, highFreqOfInterest, ampGainBW, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtOneHz, inoiseAtHighHz, atFreq=None, iNoiseAtOpAmpFreq=None):
    """Calculates integrated noise of inverting op-amp topology.

    Args:
        Rsource: Source resistance
        rOne: Input resistor
        rTwo: Feedback resistor 
        rThree: Noninverted input resistor (which is usally tied to GND)
        lowFreqOfInterest: low frequency of user interest
        highFreqOfInterest: high frequency of user interest
        ampGainBW: op-amp unity gain bandwidth (based on datasheet)
        vnoiseAtOneHz: op-amp voltage noise at low freq (based on datasheet)
        vnoiseAtHighHz: op-amp voltage noise at high freq (based on datasheet)
        inoiseAtOneHz: op-amp current noise at low freq (based on datasheet)
        inoiseAtHighHz: op-amp current noise at high freq (based on datasheet)
        atFreq: user specified frequency
        iNoiseAtOpAmpFreq: (specific to JFET-input type op-amps) current noise increase with freq (based on datasheet), default=0
    
    Returns:
        maxNoiseBW: maximum noise bandwidth
        integradedNoise: integrated noise over user's frequency of interest
    """
    atFreq = 1000 if atFreq is None else atFreq  # set atFreq to 1 kHz as default
    iNoiseAtOpAmpFreq = 0 if iNoiseAtOpAmpFreq is None else iNoiseAtOpAmpFreq # set iNoiseAtOpAmpFreq to 0 as default
    gain = rTwo / rOne
    maxNoiseBW = 1.57 * ampGainBW / gain
    RnoninvertedNoise = resistorNoise(rThree)  # V/sqrt(Hz)
    RfeedbackNoise = resistorNoise(rTwo) / gain  # V/sqrt(Hz)
    RinNoise = resistorNoise(rOne)  # V/sqrt(Hz)
    RsourceNoise = resistorNoise(Rsource)  # V/sqrt(Hz)
    # Op-amp specific parameters based on datasheet
    ampVoltNoise = opampVNoiseAtFreq(vnoiseAtOneHz, vnoiseAtHighHz, atFreq)
    ampCurrentNoise = opampINoiseAtFreq(inoiseAtOneHz, inoiseAtHighHz, atFreq, iNoiseAtOpAmpFreq)
    
    if maxNoiseBW < highFreqOfInterest:
        RsourceIntegratedNoise = RsourceNoise * np.sqrt(maxNoiseBW - lowFreqOfInterest) # Vrms
        RinIntegratedNoise = RinNoise * np.sqrt(maxNoiseBW - lowFreqOfInterest) # Vrms
        RfeedbackIntegratedNoise = np.sqrt(maxNoiseBW - lowFreqOfInterest) * RfeedbackNoise / gain # Vrms
        RnoninvertedIntegratedNoise = RnoninvertedNoise * np.sqrt(maxNoiseBW - lowFreqOfInterest) # Vrms
    else:
        RsourceIntegratedNoise = RsourceNoise * np.sqrt(highFreqOfInterest - lowFreqOfInterest) # Vrms
        RinIntegratedNoise = RinNoise * np.sqrt(highFreqOfInterest - lowFreqOfInterest) # Vrms
        RfeedbackIntegratedNoise = np.sqrt(highFreqOfInterest - lowFreqOfInterest) * RfeedbackNoise / gain # Vrms
        RnoninvertedIntegratedNoise = RnoninvertedNoise * np.sqrt(highFreqOfInterest - lowFreqOfInterest) # Vrms
    
    noninvertedInputIntegratedNoise = ampVoltNoise # Vrms, direct contribution in inverted topology
    invertedInputIntegratedNoise = ampCurrentNoise * rOne * rTwo / (rOne + rTwo) # Vrms
    
    integradedNoise = gain * np.sqrt(np.square(RsourceIntegratedNoise) + np.square(RinIntegratedNoise) + np.square(RfeedbackIntegratedNoise) + np.square(RnoninvertedIntegratedNoise) + np.square(noninvertedInputIntegratedNoise) + np.square(invertedInputIntegratedNoise))  # Vrms
    return maxNoiseBW, integradedNoise
