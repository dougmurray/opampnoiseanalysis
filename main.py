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
    while True:
        try:
            choice = int(input("Noise of (1) op-amp, (2) inverting topology, or (3) non-inverting topology: "))
        except ValueError:
            print("Please choose options 1, 2, or 3.")
            continue
        else:
            if choice == 1:
                vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, iNoiseAtHz = opampChooseInput()
                freq, vNoise, iNoise = opAmpNoise(vNoiseOneHz, vNoiseHighHz, iNoiseOneHz, iNoiseHighHz, iNoiseAtHz)
                print(freq, vNoise, iNoise)
                genericOpAmpNoisePlot(freq, vNoise, iNoise)
            elif choice == 2:
                try:
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
                    ampGainBW = float(input("Input op-amp unity gain BW (Hz): "))
                    vnoiseAtOneHz = float(input("Input op-amp Vnoise @ 1 Hz (V/sqrt(Hz): "))
                    vnoiseAtHighHz = float(input("Input op-amp Vnoise @ 10 MHz (V/sqrt(Hz): "))
                    inoiseAtOneHz = float(input("Input op-amp Inoise @ 1 Hz (A/sqrt(Hz): "))
                    inoiseAtHighHz = float(input("Input op-amp Inoise @ 10 MHz (A/sqrt(Hz): "))
                    iNoiseAtOpAmpFreq = float(input("Input op-amp Inoise freq (default = 0 Hz): "))
                except ValueError:
                    print("Invalid input")
                else:
                    invertingRTINoise(Rsource, rOne, rTwo, rThree, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtOneHz, inoiseAtHighHz, atFreq, iNoiseAtOpAmpFreq)
                    invertingIntegratedNoise(Rsource, rOne, rTwo, rThree, lowFreqOfInterest, highFreqOfInterest, ampGainBW, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtOneHz, inoiseAtHighHz, atFreq, iNoiseAtOpAmpFreq)
                    invertingNoisePlot(Rsource, rOne, rTwo, vnoiseAtOneHz, vnoiseAtHighHz, inoiseAtOneHz, inoiseAtHighHz, iNoiseAtOpAmpFreq)
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
