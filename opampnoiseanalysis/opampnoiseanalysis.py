#!/usr/bin/env python3
""" Operational Amplifier Noise Calculation and Comparison

The comparision of op-amp noise is based on
Analog Devices AN-940 Application Note: Low Noise Amplifier Selection Guide for Optimal Noise Performance.

Author: Douglass Murray

"""
import numpy as np
import matplotlib.pyplot as plt

source_resistance_scale = np.linspace(10, 1e6) # 10 - 1M Ohms
voltage_noise_scale = np.linspace(0.1, 100) # nV/sqrt(Hz)
# Resistor Johnson thermal noise
k = 1.38e-23 # J/K, Boltzmann's constant
T = 293.15 # K, 20 C in K
R = np.linspace(10, 1e6) # 10 - 1M Ohms
B = 1 # Hz, (1kHz Bandwidth?)
V_n = np.array([])
for i, element in enumerate(R):
    res_noise = np.sqrt(4 * k * T * B * element)
    V_n = np.append(V_n, res_noise)

# For 100 Ohm source reference
source_res = 100
ref_res_noise = np.sqrt(4 * k * T * B * source_res) # V/sqrt(Hz), 100 Ohms

# Op-amp noise comparison to source resistance.  
# Rs = input-referred_voltage_noise / input-referred_current_noise
# Example op-amp
ADA4898_volt_noise = 0.85e-9 # V/sqrt(Hz)
ADA4898_current_noise = 2.5e-12 # A/sqrt(Hz)
ADA4898_Rs = ADA4898_volt_noise / ADA4898_current_noise # Ohms

# Comparison plotting
plt.loglog(R, V_n, label="Johnson noise")
plt.hlines(ref_res_noise, xmin=100, xmax=10e6, linestyles="dashed", label="100 Ohms") # 100 Ohm source reference
plt.scatter(ADA4898_Rs, ADA4898_volt_noise,  label="ADA4898 not used")
plt.xlabel("Source Resistance (Ohms)")
plt.ylabel("Noise (V/sqrt(Hz))")
plt.title("Spectral Noise Density")
plt.grid(True, which="minor")
plt.legend()
plt.show()