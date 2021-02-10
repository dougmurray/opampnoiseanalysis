#!/usr/bin/env python3
""" Operational Amplifier Noise Calculator

Allows one to check out noise of op-amps in different topologies.

Author: Douglass Murray

"""
from opampnoiseanalysis.opampnoise import *
from opampnoiseanalysis.inverting import *
from opampnoiseanalysis.plotter import *

def interface():
    """General interface function for choosing which op-amp/topology to
        calculate noise."""
    while True:
        try:
            choice = int(input("Noise of (1) op-amp, (2) inverting topology, "
                               "or (3) non-inverting topology: "))
        except ValueError:
            print("Please choose options 1, 2, or 3.")
            continue
        else:
            if choice == 1:
                vnoise_low_hz, vnoise_high_hz, inoise_low_hz, inoise_high_hz,
                inoise_at_hz, amp_gain_bandwidth = opamp_choose_input()
                freq, vnoise, inoise = opamp_noise(vnoise_low_hz,
                                                   vnoise_high_hz,
                                                   inoise_low_hz,
                                                   inoise_high_hz,
                                                   inoise_at_hz,
                                                   amp_gain_bandwidth)
                print(freq, vnoise, inoise)
                generic_opamp_noise_plot(freq, vnoise, inoise)
            elif choice == 2:
                inverting_topo_image_display()
                # Topology specific parameters
                temp = float(input("Input temp (C): "))
                r_source = float(input("Input r_source (Ohm): "))
                r_one = float(input("Input R1 (Ohm): "))
                r_two = float(input("Input R2 (Ohm): "))
                r_three = float(input("Input R3 (Ohm): "))
                at_freq = float(input("Input reference freq (Hz), "
                                      "default 1000: "))
                low_freq_of_interest = float(input("Input lower freq of "
                                                   "interest (Hz): "))
                high_freq_of_interest = float(input("Input upper freq of "
                                                    "interest (Hz): "))

                # Op-amp specific parameters based on datasheet
                vnoise_low_hz, vnoise_high_hz, inoise_low_hz, inoise_high_hz,
                inoise_at_hz, amp_gain_bandwidth = opamp_choose_input()

                # Integrated noise over frequency
                max_noise_bandwidth, integrated_noise = inverting_integrated_noise(r_source,
                    r_one, r_two, r_three,
                    low_freq_of_interest, high_freq_of_interest,
                    amp_gain_bandwidth, vnoise_low_hz, vnoise_high_hz,
                    inoise_low_hz, inoise_high_hz, at_freq, inoise_at_hz,
                    temp)
                print("Max Noise BW:", max_noise_bandwidth, " Hz")
                print("Noise over bandwidth: ", integrated_noise, " Vrms")

                # Totatl RTI noise
                rti_noise = inverting_rti_noise(r_source, r_one, r_two,
                                                r_three, vnoise_low_hz,
                                                vnoise_high_hz,
                                                inoise_low_hz,
                                                inoise_high_hz,
                                                at_freq, inoise_at_hz,
                                                temp)
                print("RTI Noise: ", rti_noise, " V/sqrt(Hz)")
            elif choice == 3:
                noninverting_topo_image_display()
                noninverting_topo()
                # noisePlotter(freq, vnoise, inoise) generic noise plotter
            else:
                print("Please choose options 1, 2, or 3.")
                continue

if __name__ == '__main__':
    print(r"   ____           ___                       _   __      _              ______      __    ")
    print(r"  / __ \____     /   |  ____ ___  ____     / | / /___  (_)_______     / ____/___ _/ /____")
    print(r" / / / / __ \   / /| | / __ `__ \/ __ \   /  |/ / __ \/ / ___/ _ \   / /   / __ `/ / ___/")
    print(r"/ /_/ / /_/ /  / ___ |/ / / / / / /_/ /  / /|  / /_/ / (__  )  __/  / /___/ /_/ / / /__  ")
    print(r"\____/ .___/  /_/  |_/_/ /_/ /_/ .___/  /_/ |_/\____/_/____/\___/   \____/\__,_/_/\___/  ")
    print(r"    /_/                       /_/                                                       " )

    interface()
