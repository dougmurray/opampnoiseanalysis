#!/usr/bin/env python3
""" Operational Amplifier Noise Calculator

Allows one to check out noise of op-amps in different topologies.

Author: Douglass Murray

"""
import numpy as np
import pandas as pd
from opampnoiseanalysis.opampnoise import *
from opampnoiseanalysis.inverting import *
from opampnoiseanalysis.plotter import *

def interface():
    """General interface function for choosing which op-amp/topology to calculate noise."""
    while True:
        try:
            choice = int(input("Noise of (1) op-amp, (2) inverting topology, or (3) non-inverting topology: "))
        except ValueError:
            print("Please choose options 1, 2, or 3.")
            continue
        else:
            if choice == 1:
                vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, iNoiseAtHz, ampGBW = opampChooseInput()
                freq, vNoise, iNoise = opAmpNoise(vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, iNoiseAtHz, ampGBW)
                print(freq, vNoise, iNoise)
                genericOpAmpNoisePlot(freq, vNoise, iNoise)
            elif choice == 2:
                invertingTopoImageDisplay()
                temp = float(input("Input temp (C): "))
                Rsource = float(input("Input Rsource (Ohm): "))
                rOne = float(input("Input R1 (Ohm): "))
                rTwo = float(input("Input R2 (Ohm): "))
                rThree = float(input("Input R3 (Ohm): "))
                atFreq = float(input("Input center freq (Hz): "))
                lowFreqOfInterest = float(input("Input lower freq of interest (Hz): "))
                highFreqOfInterest = float(input("Input upper freq of interest (Hz): "))

                # Op-amp specific parameters based on datasheet
                vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, iNoiseAtHz, ampGainBW = opampChooseInput()

                # Integrated noise over frequency
                maxNoiseBW, integradedNoise = invertingIntegratedNoise(Rsource, rOne, rTwo, rThree, lowFreqOfInterest, highFreqOfInterest, ampGainBW, vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, atFreq, iNoiseAtHz, temp)
                print("Max Noise BW:", maxNoiseBW, " Hz")
                print("Noise over bandwidth: ", integradedNoise, " Vrms")
                
                # Totatl RTI noise
                RTINoise = invertingRTINoise(Rsource, rOne, rTwo, rThree, vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, atFreq, iNoiseAtHz, temp)
                print("RTI Noise: ", RTINoise, " V/sqrt(Hz)")
            elif choice == 3:
                noninvertingTopoImageDisplay()
                noninvertingTopop()
                # noisePlotter(freq, vNoise, iNoise)  # TODO: generic noise plotter
            else:
                print("Please choose options 1, 2, or 3.")
                continue

if __name__ == '__main__':
    print("   ____           ___                       _   __      _              ______      __    ")
    print("  / __ \____     /   |  ____ ___  ____     / | / /___  (_)_______     / ____/___ _/ /____")
    print(" / / / / __ \   / /| | / __ `__ \/ __ \   /  |/ / __ \/ / ___/ _ \   / /   / __ `/ / ___/")
    print("/ /_/ / /_/ /  / ___ |/ / / / / / /_/ /  / /|  / /_/ / (__  )  __/  / /___/ /_/ / / /__  ")
    print("\____/ .___/  /_/  |_/_/ /_/ /_/ .___/  /_/ |_/\____/_/____/\___/   \____/\__,_/_/\___/  ")
    print("    /_/                       /_/                                                       " )
    
    interface()
