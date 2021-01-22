#!/usr/bin/env python3
""" Operational Amplifier Noise Model

Takes op-amp intrinsic properties as inputs and outputs voltage
and current noise over 1 - 1 MHz frequency range.

Author: Douglass Murray

"""
import numpy as np
import pandas as pd
from opampnoiseanalysis.plotter import *

# freqRange = np.array([1, 2, 5, 10, 22, 46, 100, 215, 463, 1000, 2150, 4630, 10000, 21500, 46300, 100000, 215000, 463000, 1000000])
# opAmpVnoise = np.array([])
# opAmpInoise = np.array([])
# vnoiseAtOneHz = 50e-9  # V/sqrt(Hz)
# vnoiseAtHighHz = 8.0e-9  # V/sqrt(Hz)
# inoiseAtOneHz = 200e-12  # A/sqrt(Hz)
# inoiseAtHighHz = 1050e-12  # A/sqrt(Hz)
# iNoiseAtOpAmpFreq = 0  # Hz
# uGBW = 1.0e6 # Hz


def opAmpNoise(vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtOneHz, inoiseAtHighHz, iNoiseAtOpAmpFreq=None, ampGBW=None):
    """Op-amp intrinsic noise calculation.

    Args:
        vnoiseAtOneHz: op-amp voltage noise at low freq (based on datasheet)
        vnoiseAtHighHz: op-amp voltage noise at high freq (based on datasheet)
        inoiseAtOneHz: op-amp current noise at low freq (based on datasheet)
        inoiseAtHighHz: op-amp current noise at high freq (based on datasheet)
        iNoiseAtOpAmpFreq: (specific to JFET-input type op-amps) current noise increase with freq (based on datasheet), default=0

    Returns:
        freqRange: frequency range, 1 - 1 MHz (Hz)
        opAmpVnoise: op-amp voltage noise at frequencies in range (V/sqrt(Hz))
        opAmpInoise: op-amp current noise at frequencies in range (A/sqrt(Hz))
    """
    iNoiseAtOpAmpFreq = 0 if iNoiseAtOpAmpFreq is None else iNoiseAtOpAmpFreq  # set iNoiseAtOpAmpFreq to 0 as default
    ampGBW = 1e6 if ampGBW is None else ampGBW # set unity gain bandwidth to resonable default if not included
    freqRange = np.array([1, 2, 5, 10, 22, 46, 100, 215, 463, 1000,
                          2150, 4630, 10000, 21500, 46300, 100000, 215000, 463000, 1000000])
    opAmpVnoise = np.array([])
    opAmpInoise = np.array([])
    for i, element in enumerate(freqRange):
        vNoise = np.sqrt(np.square(vnoiseAtHighHz) + np.square(vnoiseAtOneHz) / element)
        opAmpVnoise = np.append(opAmpVnoise, vNoise)

    for i, element in enumerate(freqRange):
        if not iNoiseAtOpAmpFreq:
            iNoise = np.sqrt(np.square(inoiseAtOneHz) + np.square(inoiseAtHighHz) / element)
            opAmpInoise = np.append(opAmpInoise, iNoise)
        else:
            # This is a little off
            iNoise = np.sqrt(np.square(inoiseAtOneHz) + np.square(inoiseAtHighHz) * np.square(element) / np.square(iNoiseAtOpAmpFreq))
            opAmpInoise = np.append(opAmpInoise, iNoise)
    
    return freqRange, opAmpVnoise, opAmpInoise

def opampVNoiseAtFreq(vnoiseAtOneHz, vnoiseAtHighHz, atFreq=None):
    """Op-amp intrinsic voltage noise calculation at specified frequency.

    Args:
        atFreq: specified frequency, default=1000 (Hz)
        vnoiseAtOneHz: op-amp voltage noise at low freq (based on datasheet) 
        vnoiseAtHighHz: op-amp voltage noise at high freq (based on datasheet)

    Returns:
        opampVnoiseAtFreq: op-amp voltage noise at specified frequency (V/sqrt(Hz))
    """
    atFreq = 1000 if atFreq is None else atFreq  # set atFreq to 1 kHz as default
    opampVnoiseAtFreq = np.sqrt(np.square(vnoiseAtHighHz) + np.square(vnoiseAtOneHz) / atFreq)
    return opampVnoiseAtFreq

def opampINoiseAtFreq(inoiseAtOneHz, inoiseAtHighHz, atFreq=None, iNoiseAtOpAmpFreq=None):
    """Op-amp intrinsic current noise calculation at specified frequency.

    Args:
        atFreq: specified frequency, default=1000 (Hz)
        inoiseAtOneHz: op-amp current noise at low freq (based on datasheet)
        inoiseAtHighHz: op-amp current noise at high freq (based on datasheet)
        iNoiseAtOpAmpFreq: (specific to JFET-input type op-amps) current noise increase with freq (based on datasheet), default=0

    Returns:
        opampINoiseAtFreq: op-amp current noise at specified frequency (A/sqrt(Hz))
    """
    atFreq = 1000 if atFreq is None else atFreq  # set atFreq to 1 kHz as default
    iNoiseAtOpAmpFreq = 0 if iNoiseAtOpAmpFreq is None else iNoiseAtOpAmpFreq
    if not iNoiseAtOpAmpFreq:
        opampINoiseAtFreq = np.sqrt(np.square(inoiseAtOneHz) +
                         np.square(inoiseAtHighHz) / atFreq)
    else:
        opampINoiseAtFreq = np.sqrt(np.square(inoiseAtOneHz) + np.square(
            inoiseAtHighHz) + np.square(element) / np.square(iNoiseAtOpAmpFreq))
    return opampINoiseAtFreq

def opampChooseInput():
    """Helper function for user to choose between inputing discrete vlaues or import via csv file.

    Args:
        None
    
    Returns:
        vNoiseOneHz: op-amp voltage noise at low freq (based on datasheet) 
        vNoiseHighHz: op-amp voltage noise at high freq (based on datasheet)
        iNoiseOneHz: op-amp current noise at low freq (based on datasheet)
        iNoiseHighHz: op-amp current noise at high freq (based on datasheet)
        iNoiseAtHz: (specific to JFET-input type op-amps) current noise increase with freq (based on datasheet), default=0
        ampGBW: op-amp unity gain bandwidth
    """
    opampChoice = int(input("Input (1) op-amp values or (2) pick op-amp: "))
    if opampChoice == 1:        
        # direct input of op-amp values
        vNoiseOneHz = float(input("Vnoise @ 1 Hz: "))
        vNoiseHighHz = float(input("Vnoise @ 10 MHz: "))
        iNoiseOneHz = float(input("Inoise @ 1 Hz: "))
        iNoiseHighHz = float(input("Inoise @ 10 MHz: "))
        iNoiseAtHz = float(input("Inoise Freq (default = 0): "))
        ampGBW = float(input("Input op-amp unity gain BW (Hz): "))
    elif opampChoice == 2:
        opampName = str(input("Input op-amp name: "))
        # Search and pick op-amp
        # csv format: Device, VnoiseLow, VnoiseHigh, InoiseLow, InoiseHigh, InoiseSpecFreq, UGBW
        opamps = pd.read_csv('./opampdata/opampData.csv')
        oneAmp = opamps.loc[opamps['Device'] == opampName]
        # if Pandas version is < version 0.24
        specificAmp = oneAmp.values
        # if Pandas version is > version 0.24
        # specificAmp = oneAmp.to_numpy(copy=True)
        vNoiseOneHz = specificAmp[0, 1]
        vNoiseHighHz = specificAmp[0, 2]
        iNoiseOneHz = specificAmp[0, 3]
        iNoiseHighHz = specificAmp[0, 4]
        iNoiseAtHz = specificAmp[0, 5]
        ampGBW = specificAmp[0,6]
    else:
        print("Please choose either (1) op-amp values or (2) pick op-amp.")
    return vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, iNoiseAtHz, ampGBW
