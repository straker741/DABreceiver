# Autor: Jakub Svajka
# Datum: 22.3.2020

# -------------------------------------- EXTERNAL LIBRARIES ------------------------------------- #
from rtlsdr import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt     # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.html
import subprocess                   # https://docs.python.org/2/library/subprocess.html

# ---------------------------------------- MY LIBRARIES ------------------------------------------ #
import mySimpleMathLib

# ---------------- GLOBAL VARIABLES ----------------- #
hodnoty = []
frekvencie = []
number_of_FFT = 1024
f0 = int(number_of_FFT / 2)
rozsah = int(number_of_FFT / 16)     # Bulharska konstanta = 64

def fHrany(midValue):
    """
    Funkcia prehladava cely zoznam hodnot a porovnava ich s hodnotou midValue (Stredna hodnota aktivnej casti signalu).
    """
    global hodnoty, frekvencie
    f1 = 0
    f2 = 0
    if midValue == 0:
        print("Error: Stredna hodnota je nulova.")
    else:
        samples = len(frekvencie)
        # Ak prekroci strednu hodnotu zlava  (ideme od zaciatku)  => nasli sme 1. frekvenciu      (_/)
        for i in range(samples):
            if midValue <= hodnoty[i]:           
                f1 = i
                break
        # Ak prekroci strednu hodnotu zprava (ideme od konca)     => nasli sme 2. frekvenciu      (\_)
        for i in range(samples):
            j = samples - i - 1
            if midValue <= hodnoty[j]:           
                f2 = j
                break            
    return f1, f2

# --------------------- POWER SPECTRAL DENSITY -------------------------- #
# This describes how power of a signal or time series is distributed over frequency 
def doPSD(sdr, centerFrequency):
    """ Odcita vzorky, ktore potom spracuje a vykresli do grafu.
        Funkcia konci ulozenim grafu do .png formatu a ukoncenim kernel modulu."""

    global hodnoty, frekvencie
    # configuring device
    sdr.sample_rate = 2.4e6
    sdr.center_freq = centerFrequency
    sdr.gain = 7.1              # Podporovane hodnoty gain: [-9.9; -4; 7.1; 17.9; 19.2]

    samples = sdr.read_samples(number_of_FFT*256) # == 262 144 komplexnych cisel

    # Using matplotlib.pyplot to estimate and plot the Power Spectral Density
    result = plt.psd(samples, NFFT=number_of_FFT, Fs=sdr.sample_rate, Fc=sdr.center_freq)

    hodnoty = result[0]         # 'hodnoty' predstavuju vykon a maju absolutnu velkost
    frekvencie = result[1]      # 'frekvencie' su hodnoty prisluchajuce jednotlivym hodnotam 'hodnoty'
    
    # Save figure (Line2D object)
    # Urobi graf: ['frekvencie', 'hodnoty'] ale hodnoty su uz premenene na db ako 10*log_10(hodnoty[_])
    plt.savefig('/var/www/html/obrazky/power_spectral_density.png')
    # Clearing figure
    plt.clf()

def checkBandwidth(sdr, centerFrequency): 
    global hodnoty, frekvencie
    
    doPSD(sdr, centerFrequency)     # Do Power Spectral Density

    # ----------------------- SPRACOVANIE HODNOT ------------------------------- #
    # Priemerujem oblasti aktivneho signalu a sumu
    
    centerAVG = mySimpleMathLib.AVG(hodnoty[f0-rozsah*4 : f0+rozsah*4])
    noiseAVG = (mySimpleMathLib.AVG(hodnoty[ :rozsah*3]) + mySimpleMathLib.AVG(hodnoty[-rozsah*3: ])) / 2
    
    # Zistujem strednu hodnotu hodnot 'centerAVG' a 'noiseAVG', aby som vedel urcit poziciu nabeznej a dobeznej hrany
    middleValue = (centerAVG - noiseAVG) / 2

    # Hladam ktore frekvencie sa priblizuju vypocitanej hodnote 'middleValue'
    f1, f2 = fHrany(middleValue)
    # f1 a f2 su index frequencii "nabeznej" a "dobeznej" hrany
    return frekvencie[f2] - frekvencie[f1]