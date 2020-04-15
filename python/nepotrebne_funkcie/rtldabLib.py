# Autor: Jakub Svajka
# Datum: 7.3.2020

import subprocess       # https://docs.python.org/2/library/subprocess.html

def rFile(path):
    """Read from a file."""
    try:
        with open(path, 'r') as f:    
            content = f.read()
        return content
    except:
        print("Error: Could not read from a file.")
        return False
    pass

def wFile(path, content=None):
    """Write to a file."""
    try:
        with open(path, 'w') as f:    
            if content == None:
                return f
            else:
                f.write(content)
                return True
    except:
        print("Error: Could not write to a file.")
        return False
    pass

def getCenterFrequency():
    """Frequency from file which is operated via web interface."""
    # tuner: Fitipower FC0012
    lowLimit = int(22 * 1e6)     # 22.00 MHz
    highLimit = int(948.6 * 1e6) # 948.6 MHz

    centerFrequency = rFile("/var/www/html/frequency.txt")
    #centerFrequency = rFile("C:/Users/Jakub/Desktop/SKOLA/Bakalarka/html/frequency.txt")

    if centerFrequency == False:
        centerFrequency = 227360000 # Kamzik - Bratislava
    else:      
        try:
            centerFrequency = int(centerFrequency)
            if not (lowLimit < centerFrequency < highLimit):
                # Frequency is not in the limit!
                centerFrequency = 227360000 # Kamzik - Bratislava
        except ValueError:
            print("{getCentralFrequency} Error: centerFrequency is not a number!")
            print("Setting centerFrequency 227.360 MHz!")
            centerFrequency = 227360000 # Kamzik - Bratislava
    return centerFrequency
    pass

def getData():
    transmitterName = ''
    ber = 0.0
    # Getting frequency
    frequency = getCenterFrequency()
    cmd = "sudo ~/rtl-dab/src/rtldab " + str(frequency)
    # Executing command - oppening pipe
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)

    with open("rtldab_out.txt", "w") as f:
        save = False
        for lStr in p.stderr:
            # Reading output line by line
            lList = lStr.split()
            if lList == []:
                continue

            if((not save) and (lList[0] == "cts")):
                save = True
            elif(save and (lList[0] == "User")):
                save = False

            if save:               
                f.write(lStr)
                # Writing to file for further proccessing on the web
                if lList[0] == "channel":
                    ber = float(lList[2])
                    # Bit Error Ratio
                elif lList[0] == "Subchannel":
                    transmitterName = ''
                    # Name of the transmitter (should be TOWERCOM in our case)
                    pass
    return transmitterName, ber
    pass

def is_in(a, b):
    if b in a:
        return True
    return False
    pass

if __name__ == "__main__":
    print("Start of the test.")
    getData()
    print("End of the test.")
    pass