#!/usr/bin/env python3
""" Inverting Operational Amplifier Noise Calculation

Takes into account all the noise sources in an inverting topology.

Author: Douglass Murray

"""
import os
import numpy as np
import matplotlib.image as img
# from opampnoiseanalysis.o   import opampnoise
from opampnoiseanalysis.opampnoise import *

def invertingTopoImageDisplay():
    os.system("open ../images/inverting.png")  # Will open in Preview.

def resistorNoise(resistor, temp=None):
    # Resistors Johnson thermal noise
    temp = 20 if temp is None else temp # set temp at room temp as default
    k = 1.38e-23  # J/K, Boltzmann's constant
    resistorVoltageNoise = np.sqrt(4 * k * (temp + 273) * resistor)  # V/sqrt(Hz)
    return resistorVoltageNoise

# RTI Total Noise (V/sqrt(Hz))


def invertingRTINoise(Rsource, rOne, rTwo, rThree, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtHighHz, inoiseAtOneHz, atFreq=None, iNoiseAtOpAmpFreq=None):
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
    print("Noise RTI: ", RTINoise, " V/sqrt(Hz)")
    # return RTINoise

# Integrated Noise over frequency (Vrms)
def invertingIntegratedNoise(Rsource, rOne, rTwo, rThree, lowFreqOfInterest, highFreqOfInterest, ampGainBW, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtHighHz, inoiseAtOneHz, atFreq=None, iNoiseAtOpAmpFreq=None):
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
    
    print("Max Noise BW:", maxNoiseBW, " Hz")
    print("Noise over bandwidth: ", integradedNoise, " Vrms")
    # return integradedNoise
