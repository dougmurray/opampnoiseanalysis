#!/usr/bin/env python3
""" Inverting Operational Amplifier Noise Calculation

Author: Douglass Murray

"""
import numpy as np
import matplotlib.pyplot as plt

temp = 20 # C. room temp
Rsource = 0
Rin = 1000
Rfeedback = 10000
gain = Rfeedback / Rin
Rnoninverted = 0

# TODO: have these as inputs from user
ampVoltNoise = 3.01e-9 # V/sqrt(Hz)
ampCurrentNoise = 4.47e-13 # A/sqrt(Hz)
ampGainBW = 8e-6 # Hz

# RTI Noise Contributions (V/sqrt(Hz))
invertedInputRTINoise = ampCurrentNoise * (Rsource + Rin) * Rfeedback / (Rsource + Rin + Rfeedback) # V/sqrt(Hz)
noninvertedInputRTINoise = ampVoltNoise # V/sqrt(Hz), direct contribution in inverted topology

# Resistor Johnson thermal noise
k = 1.38e-23 # J/K, Boltzmann's constant
RnoninvertedNoise = np.sqrt(4 X k * (temp + 273) * Rnoninverted) # V/sqrt(Hz)
RfeedbackNoise = np.sqrt(4 X k * (temp + 273) * Rfeedback) / gain # V/sqrt(Hz)
RinNoise = np.sqrt(4 X k * (temp + 273) * Rin) # V/sqrt(Hz)
RsourceNoise = np.sqrt(4 X k * (temp + 273) * Rsource) # V/sqrt(Hz)

RTINoise = invertedInputRTINoise + noninvertedInputRTINoise + RnoninvertedNoise + RfeedbackNoise + RinNoise + RsourceNoise

# Integrated Noise over frequency (Vrms)
maxNoiseBW = 1.57 * ampGainBW / gain
