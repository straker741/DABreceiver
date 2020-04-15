# Autor:    Jakub Svajka

# -------------------------------------- EXTERNAL LIBRARIES ------------------------------------- #
from rtlsdr import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt     # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.html

import time
import MySQLdb
#import numpy as np                  # https://docs.scipy.org/doc/numpy-1.13.0/reference/index.html
#import scipy                        # https://docs.scipy.org/doc/scipy-0.18.1/reference/index.html

# ---------------------------------------- MY LIBRARIES ------------------------------------------ #
import mySimpleMathLib
import rtldabLib
# ---------------- FUNCTIONS ----------------- #

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

def writeToDB(transmitterName, bandwidth, ber, signalPower, noisePower):
    """databaza: signals --- id | transmitterName | bandwidth | bit error ratio | signalPower | noisePower? | datetime"""
    try:
        # Checking whether variable 'signalPower' is a number
        signalPower = float(signalPower)

        # Connecting to database
        db = MySQLdb.connect(host="localhost", user="root", passwd="", db="bakalarka")
        cursor = db.cursor()

        # Building query
        loggit = "INSERT INTO signals (transmitterName, bandwidth, bit error ratio, signalPower, noisePower) VALUES (%s, %s, %s, %s, %s)"

        # Executing query
        cursor.execute(loggit, [transmitterName, bandwidth, ber, signalPower, noisePower])
        db.commit()
        return True        
    except:
        print("{writeToDB} Error: Writing to database was not successful.")
        return False
    pass

# --------------------- POWER SPECTRAL DENSITY -------------------------- #
# This describes how power of a signal or time series is distributed over frequency 
def doPSD():
    """ Spusti kernel modul, ktory odcita vzorky. Vzorky spracuje a vykresli do grafu.
        Funkcia konci ulozenim grafu do .png formatu a ukoncenim kernel modulu.         """
    try:
        # Starting kernel module
        sdr = RtlSdr()

        centerFrequency = rtldabLib.getCenterFrequency()

        # configuring device
        sdr.sample_rate = 2.4e6
        sdr.center_freq = centerFrequency
        sdr.gain = 7.1              # Podporovane hodnoty gain: [-9.9; -4; 7.1; 17.9; 19.2]

        samples = sdr.read_samples(number_of_FFT*256) # == 262 144 komplexnych cisel

        # Using matplotlib.pyplot to estimate and plot the Power Spectral Density
        result = plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate, Fc=sdr.center_freq)

        hodnoty = result[0]         # 'hodnoty' predstavuju vykon a maju absolutnu velkost
        frekvencie = result[1]      # 'frekvencie' su hodnoty prisluchajuce jednotlivym hodnotam 'hodnoty'
        
        # Save figure (Line2D object)
        # Urobi graf: ['frekvencie', 'hodnoty'] ale hodnoty su uz premenene na db ako 10*log_10(hodnoty[_])
        plt.savefig('/var/www/html/obrazky/power_spectral_density.png')
        # Clearing figure
        plt.clf()
        # Closing kernel module
        sdr.close()
    except:
        print("Exception at function {doPSD}.")
    pass

##################################################################################

# ------------------------- CONSTANTS & GLOBAL VARIABLES ------------------------------- #
hodnoty = []
frekvencie = []
number_of_FFT = 1024
f0 = int(number_of_FFT / 2)
rozsah = int(number_of_FFT / 16)     # Bulharska konstanta = 64
T_DAB_radio = 5                 # Jedna perioda celeho skriptu bude trvat 5 sekund

try:
    while True:
        start = time.time()
        
        doPSD()       
        
        # ----------------------- SPRACOVANIE HODNOT ------------------------------- #
        # Priemerujem oblasti aktivneho signalu a sumu
        
        centerAVG = mySimpleMathLib.AVG(hodnoty[f0-rozsah*4 : f0+rozsah*4])
        noiseAVG = (mySimpleMathLib.AVG(hodnoty[ :rozsah*3]) + mySimpleMathLib.AVG(hodnoty[-rozsah*3: ])) / 2
        
        # Zistujem strednu hodnotu hodnot 'centerAVG' a 'noiseAVG', aby som vedel urcit poziciu nabeznej a dobeznej hrany
        middleValue = (centerAVG - noiseAVG) / 2

        # Hladam ktore frekvencie sa priblizuju vypocitanej hodnote 'middleValue'
        f1, f2 = fHrany(middleValue)
        # f1 a f2 su index frequencii "nabeznej" a "dobeznej" hrany
        
        # Spocitavam hodnoty v rozmedzi najdenych indexov frekvencii f1 a f2
        vykonSignalu = mySimpleMathLib.SUM(hodnoty[f1:f2])
        vykonSignalu *= (frekvencie[f1+1]-frekvencie[f1])   # Takto najdem sirku jedneho prirastku
        sirkaPasma = frekvencie[f2] - frekvencie[f1]
        # Konvertujem hednotu 'noiseAVG' do decibelov
        vykonSumu = mySimpleMathLib.convertToDecibel(noiseAVG)
        if vykonSumu == -1 :
            # Ak sa nepodarilo konvertovat 'noiseAVG', musime to skusit zmerat znovu
            continue

        if False:
            # MUSIM ESTE DEKODOVAT MENO STANICE ALEBO MENO VYSIELACA
            #menoStanice = "Radio Slovensko"
            #path = "C:/Users/Jakub/Desktop/Skola/Bakalarka/welle-cli_-c_12C_-p_ANTENA_ROCK_output.txt"
            #path = "C:/Users/Jakub/Desktop/Skola/Bakalarka/zoznam_radii.txt"
            if False:
                # Ak sme nasli hladanu stanicu v zozname, ukladam do databazy
                #writeToDB(vykonSignalu, vykonSumu, menoStanice, sirkaPasma )
                # Opravit vstupne premenne, nie je spravne poradie
                pass

        # ------------------ DEBUGGING ------------------------ #

        debugging = True
        if debugging:
            max = mySimpleMathLib.MAX(hodnoty)
            min = mySimpleMathLib.MIN(hodnoty)
            print("MAX:", max)
            print("log(MAX):", mySimpleMathLib.convertToDecibel(max))
            print("MIN:", min)
            print("log(MIN):", mySimpleMathLib.convertToDecibel(min))
            print("centerAVG:", centerAVG)
            print("log(centerAVG):", mySimpleMathLib.convertToDecibel(centerAVG))
            print("noiseAVG:", noiseAVG)
            print("log(noiseAVG):", mySimpleMathLib.convertToDecibel(noiseAVG))
            print("middleValue:", middleValue)
            print("log(middleValue):", mySimpleMathLib.convertToDecibel(middleValue))         
            print("integral:", vykonSignalu)


            print("frekvencie:", frekvencie[f1], frekvencie[f2])
            print("sirka_pasma:", sirkaPasma)

        end = time.time()
        time.sleep(T_DAB_radio - (end - start))   # cely cyklus bude trvat 'T_DAB_radio' sekund
        pass
except:
    print("End of DAB_radio script.")
    pass