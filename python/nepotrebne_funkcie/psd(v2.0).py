from rtlsdr import *
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

def rFile(path):
    """Reading one line from a file."""
    try:
        with open(path, 'r') as f:    
            content = f.readline()
    except:
        print("Error: Could not read from file.")
        return '522000000'  # RTVS
    return content
    pass

def maximum(array):
    
    for i in range(len(array)):
        if i == 0:
            result = array[i]
            index = 0

        if result < array[i]:
            result = array[i]
            index = i
    return result, index
    pass

def doPSD(centerFrequency):
    try:
        # configuring device
        sdr.sample_rate = sample_rate
        sdr.center_freq = centerFrequency
        sdr.gain = 7.7

        samples = sdr.read_samples(1024*256) # == 262 144 komplexnych cisel

        # using matplotlib to estimate and plot the PSD
        result = plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate, Fc=sdr.center_freq)

        hodnoty = result[0]
        frekvencie = result[1]

        if len(result) > 2:
            graf = result[2]
        
        plt.savefig('/var/www/html/obrazky/power_spectral_density.png')
        plt.clf()
    except KeyboardInterrupt:
        sdr.close()
    pass

def whiteNoise(readings = 3):

    pass

##################################################################################

hodnoty = []
frekvencie = []
sdr = RtlSdr()   
sample_rate = 2.4e6

while True:
    
    center_freq = int(rFile("/var/www/html/frequency.txt"))
    doPSD(center_freq)
        
    time.sleep(4)
    
        
    break
    pass