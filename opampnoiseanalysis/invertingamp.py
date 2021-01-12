#!/usr/bin/env python3
""" Inverting Operational Amplifier Noise Calculation

Author: Douglass Murray

"""
import numpy as np
import matplotlib.pyplot as plt

temp = 20 # C, room temp
Rsource = 0
Rin = 1000
Rfeedback = 100000
gain = Rfeedback / Rin
Rnoninverted = 0

# TODO: have these as inputs from user
ampVoltNoise = 3.01e-9 # V/sqrt(Hz)
ampCurrentNoise = 4.47e-13 # A/sqrt(Hz)
ampGainBW = 8e6 # Hz

# RTI Noise Contributions (V/sqrt(Hz))
invertedInputRTINoise = ampCurrentNoise * (Rsource + Rin) * Rfeedback / (Rsource + Rin + Rfeedback) # V/sqrt(Hz)
noninvertedInputRTINoise = ampVoltNoise # V/sqrt(Hz), direct contribution in inverted topology
# Resistors Johnson thermal noise
k = 1.38e-23 # J/K, Boltzmann's constant
RnoninvertedNoise = np.sqrt(4 * k * (temp + 273) * Rnoninverted) # V/sqrt(Hz)
RfeedbackNoise = np.sqrt(4 * k * (temp + 273) * Rfeedback) / gain # V/sqrt(Hz)
RinNoise = np.sqrt(4 * k * (temp + 273) * Rin) # V/sqrt(Hz)
RsourceNoise = np.sqrt(4 * k * (temp + 273) * Rsource) # V/sqrt(Hz)

RTINoise = gain * np.sqrt(np.square(invertedInputRTINoise) + np.square(noninvertedInputRTINoise) + np.square(RnoninvertedNoise) + np.square(RfeedbackNoise) + np.square(RinNoise) + np.square(RsourceNoise)) # V/sqrt(Hz)


# Integrated Noise over frequency (Vrms)
maxNoiseBW = 1.57 * ampGainBW / gain
lowFreqOfInterest = 1 # Hz
highFreqOfInterest = 10000 # Hz

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

integradedNoise = gain * np.sqrt(np.square(RsourceIntegratedNoise) + np.square(RinIntegratedNoise) + np.square(RfeedbackIntegratedNoise) + np.square(RnoninvertedIntegratedNoise) + np.square(noninvertedInputIntegratedNoise) + np.square(invertedInputIntegratedNoise)) # Vrms

print("Rsource: ", Rsource, " Ohms")
print("Rin: ", Rin, " Ohms")
print("Rfeedback: ", Rfeedback, " Ohms")
print("Rnoninverted: ", Rnoninverted, " Ohms")
print("Amplifier gain:", gain, " V/V")
print("Max Noise BW:", maxNoiseBW, " Hz")
print("RTI Noise: ", RTINoise, " V/sqrt(Hz)")
print("Noise over bandwidth: ", integradedNoise, " Vrms")
# print(RsourceIntegratedNoise , RinIntegratedNoise, RfeedbackIntegratedNoise, RnoninvertedIntegratedNoise, noninvertedInputIntegratedNoise, invertedInputIntegratedNoise)