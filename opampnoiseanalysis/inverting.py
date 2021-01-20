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

def resistorNoise(resistor, temp=20):
    # Resistors Johnson thermal noise
    k = 1.38e-23  # J/K, Boltzmann's constant
    resistorVoltageNoise = np.sqrt(4 * k * (temp + 273) * resistor)  # V/sqrt(Hz)
    return resistorVoltageNoise

# RTI Total Noise (V/sqrt(Hz))
def invertingRTINoise(Rsource, Rin, Rfeedback, atFreq, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtHighHz, inoiseAtOneHz, iNoiseAtOpAmpFreq):
    gain = Rfeedback / Rin
    # Op-amp specific parameters based on datasheet
    ampVoltNoise = opampVNoiseAtFreq(atFreq, vnoiseAtOneHz, vnoiseAtHighHz)
    ampCurrentNoise = opampINoiseAtFreq(atFreq, inoiseAtHighHz, inoiseAtOneHz, iNoiseAtOpAmpFreq)

    # RTI Noise Contributions (V/sqrt(Hz))
    invertedInputRTINoise = ampCurrentNoise * (Rsource + Rin) * Rfeedback / (Rsource + Rin + Rfeedback) # V/sqrt(Hz)
    noninvertedInputRTINoise = ampVoltNoise # V/sqrt(Hz), direct contribution in inverted topology
    RnoninvertedNoise = resistorNoise(Rnoninverted) # V/sqrt(Hz)
    RfeedbackNoise = resistorNoise(Rfeedback) / gain # V/sqrt(Hz)
    RinNoise = resistorNoise(Rin) # V/sqrt(Hz)
    RsourceNoise = resistorNoise(Rsource) # V/sqrt(Hz)

    RTINoise = gain * np.sqrt(np.square(invertedInputRTINoise) + np.square(noninvertedInputRTINoise) + np.square(RnoninvertedNoise) + np.square(RfeedbackNoise) + np.square(RinNoise) + np.square(RsourceNoise)) # V/sqrt(Hz)
    print("Noise RTI: ", RTINoise, " V/sqrt(Hz)")
    # return RTINoise

# Integrated Noise over frequency (Vrms)
def invertingIntegratedNoise(ampGainBW, Rin, Rfeedback, RsourceNoise, RinNoise, RnoninvertedNoise, lowFreqOfInterest, highFreqOfInterest, atFreq, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtHighHz, inoiseAtOneHz, iNoiseAtOpAmpFreq):
    gain = Rfeedback / Rin
    maxNoiseBW = 1.57 * ampGainBW / gain
    # Op-amp specific parameters based on datasheet
    ampVoltNoise = opampVNoiseAtFreq(atFreq, vnoiseAtOneHz, vnoiseAtHighHz)
    ampCurrentNoise = opampINoiseAtFreq(atFreq, inoiseAtHighHz, inoiseAtOneHz, iNoiseAtOpAmpFreq)
    
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
    invertedInputIntegratedNoise = ampCurrentNoise * Rin * Rfeedback / (Rin + Rfeedback) # Vrms
    
    integradedNoise = gain * np.sqrt(np.square(RsourceIntegratedNoise) + np.square(RinIntegratedNoise) + np.square(RfeedbackIntegratedNoise) + np.square(
        RnoninvertedIntegratedNoise) + np.square(noninvertedInputIntegratedNoise) + np.square(invertedInputIntegratedNoise))  # Vrms
    
    print("Max Noise BW:", maxNoiseBW, " Hz")
    print("Noise over bandwidth: ", integradedNoise, " Vrms")
    # return integradedNoise
