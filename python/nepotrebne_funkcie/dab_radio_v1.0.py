# ----------------------------- OPEN SOURCE OR FREE LIBRARIES ------------------------------------- #
from rtlsdr import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt     # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.html

import time
import MySQLdb
import numpy as np                  # https://docs.scipy.org/doc/numpy-1.13.0/reference/index.html
import scipy                        # https://docs.scipy.org/doc/scipy-0.18.1/reference/index.html

# ---------------------------------------- MY LIBRARIES ------------------------------------------ #
import MySimpleMath

# ---------------- FUNCTIONS ----------------- #

def rFile(path):
    """Reading one line from a file."""
    try:
        with open(path, 'r') as f:    
            content = f.readline()
        return content
    except:
        print("Error: Could not read from file.")
        return '227360000'  # Kamzik - Bratislava
    pass

def fHrany(midValue):
    """
    Funkcia prehladava cely zoznam hodnot a porovnava ich s hodnotou midValue (Stredna hodnota aktivnej casti signalu).
    Ak prekroci strednu hodnotu zlava  (ideme od zaciatku)  => nasli sme 1. frekvenciu      (_/)
    Ak prekroci strednu hodnotu zprava (ideme od konca)     => nasli sme 2. frekvenciu      (\_)
    """
    
    f1 = -1
    f2 = -1
    if midValue == 0:
        print("Error: Stredna hodnota je nulova.")
    else:
        samples = len(frekvencie)
        for i in range(samples):
            if midValue <= hodnoty[i]:           
                f1 = i
                break

        for i in range(samples):
            j = samples - i - 1
            if midValue <= hodnoty[j]:           
                f2 = j
                break            
    return f1, f2
    pass

def convertToDecibel(num):
    try:
        return 10*math.log10(num)
    except:
        print("Error. Cannot convert to decibel!")
        return -1
    pass

def modulus(arr):
    size = len(arr)
    result = [ 0 for i in range(size)]
    for i in range(size):
        result[i] = arr[i].real**2 + arr[i].imag**2
    return result
    pass

number_of_FFT = 1024
rozsah = number_of_FFT / 16     # bulharska konstanta = 64

try:  
    # Starting kernel module
    sdr = RtlSdr()
    while True:
        center_freq = int(rFile("/var/www/html/frequency.txt"))

        # Configuring device
        sdr.sample_rate = 2.4e6
        sdr.center_freq = center_freq
        sdr.gain = 4

        #samples = sdr.read_samples(number_of_FFT*256)
        samples = sdr.read_bytes(number_of_FFT*2*256)
           
        """
        Spectral Analysis: (scipy.signal)
            periodogram(x[, fs, window, nfft, detrend, …])
                - Estimate power spectral density using a periodogram.
            welch(x[, fs, window, nperseg, noverlap, …])
                - Estimate power spectral density using Welch’s method.
        """
        #m = modulus(samples)
        #np.fft.fft()

        # Plot data
        # Creating figure
        plt.figure()


        plt.plot(m, color='r', linewidth=2.0)

        
        plt.savefig('/var/www/html/obrazky/power_spectral_density.png')

        # Clear figure
        plt.clf()
        
        if False:
            # ----------------------- SPRACOVANIE HODNOT ------------------------------- #
            # Priemerujem oblasti aktivneho signalu a sumu
            f0 = int(number_of_FFT / 2)
            centerAVG = MySimpleMath.AVG(hodnoty[f0-rozsah*4 : f0+rozsah*4])
            noiseAVG = (MySimpleMath.AVG(hodnoty[ :rozsah*3]) + MySimpleMath.AVG(hodnoty[-rozsah*3: ])) / 2
        
            # Zistujem strednu hodnotu hodnot 'centerAVG' a 'noiseAVG', aby som vedel urcit poziciu nabeznej a dobeznej hrany
            middleValue = (centerAVG - noiseAVG) / 2

            # Hladam ktore frekvencie sa priblizuju vypocitanej hodnote 'middleValue'
            f1, f2 = fHrany(middleValue)
            # f1 a f2 su index frequencii nabeznej a dobeznej hrany
        
            # Spocitavam hodnoty v rozmedzi najdenych frekvencii f1 a f2
            vykonSignalu = MySimpleMath.SUM(hodnoty[f1:f2])

            # Konvertujem hednotu 'noiseAVG' do decibelov
            vykonSumu = convertToDecibel(noiseAVG)
            if vykonSumu == -1 :
                # Ak sa nepodarilo konvertovat 'noiseAVG', musime to skusit zmerat znovu
                continue

        
        
            # ------------------ DEBUGGING ------------------------ #

            debugging = True
            if debugging:
                max = MySimpleMath.MAX(hodnoty)
                min = MySimpleMath.MIN(hodnoty)
                print("MAX:", max)
                print("log(MAX):", convertToDecibel(max))
                print("MIN:", min)
                print("log(MIN):", convertToDecibel(min))
                print("centerAVG:", centerAVG)
                print("log(centerAVG):", convertToDecibel(centerAVG))
                print("noiseAVG:", noiseAVG)
                print("log(noiseAVG):", convertToDecibel(noiseAVG))
                print("middleValue:", middleValue)
                print("log(middleValue):", convertToDecibel(middleValue))         
                print("integral:", vykonSignalu)
                print("frekvencie:", frekvencie[f1], frekvencie[f2])
                print("sirka_pasma:", frekvencie[f2] - frekvencie[f1])

        time.sleep(4)   # cely vypocet trva cca 1 sekundu
        pass
except:
    sdr.close()
    pass