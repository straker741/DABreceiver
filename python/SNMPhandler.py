# Autor: Jakub Svajka
# Date:  18.4.2020

import MySQLdb
import time
import subprocess
import mySimpleMathLib

# ----------------- CONSTANTS ----------------- #
A = 0.1
thresholdBER = 0.2
thresholdSNR = 5
thresholdError = 10
thresholdBW = 1000

core_loggit  = "SELECT t1.id, t1.BER AS BER, t1.FIBER AS FIBER, t2.SNR AS SNR, t2.bandwidth AS BW, t1.datetime "
core_loggit += "FROM dabtable1 AS t1 "
core_loggit += "JOIN dabtable2 AS t2 ON t1.datetime = t2.datetime "

# ----------------- FUNCTIONS ----------------- #
def getLastDateTime():
    cursor.execute("SELECT id, datetime FROM dabtable1 WHERE id=(SELECT MAX(id) FROM dabtable1)")
    db.commit()
    data = cursor.fetchone()     
    if data is not None:
        return data[1].strftime('%Y-%m-%d %H-%M-%S')
    else:
        print("Table is empty!")
        return None

def StartUp(timeout = 30):
    """At Start table may be empty, or receiver is not adjusted and needs some time."""
    
    last_dt = getLastDateTime()
    # Firstly, wait for some data to be inserted in case we are starting the script for the very first time when the table is empty
    while not last_dt == None:
        # if last_dt == None => Table is empty!
        print("Waiting for new data.")
        time.sleep(3)                   # wait for a while
        last_dt = getLastDateTime()
    
    # Secodly, check whether new data are continuosly flowing into the table
    while True
        time.sleep(3)     # wait for a while
        if last_dt < getLastDateTime():
            break
        else:
            print("Waiting for new data.")

    # table is not empty anymore and data are continuosly flowing!
    # Give the receiver some time to adjust
    time.sleep(timeout)

def checkProcess():
    # Check how many processes with name welle-cli are running
    # Note that when starting process ps fx, total 3 and more processes are found
    p = subprocess.Popen("ps fx | grep welle-cli", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    out = p.communicate()[0].splitlines()

    if len(out) < 3:
        # No welle-cli is running
        raise Exception

def sendTrap():
    pass

# Connect to DB
try:
    db = MySQLdb.connect(host="localhost", user="stu", passwd="korona2020", db="bakalarka")
    cursor = db.cursor()
except:
    print("Could not connect to database!")
    cursor.close()
    db.close()
    exit()

try:
    StartUp(30)
    checkProcess()  # Someone may have stopped welle-cli at StartUp
    last_datetime = getLastDateTime()

    meanBER = 0
    meanSNR = 0
    error = 0
    # Main never-ending loop 
    while True:
        loggit = core_loggit + "WHERE t1.datetime > '" + last_datetime + "'"
        cursor.execute(loggit)
        db.commit()
        data = cursor.fetchall()

        # Evaluate Data and decide whether to send SNMP Trap !
        for row in data:
            # row[1] == BER         worst case:   BER >= 0.5   best case: BER   -> 0
            # row[2] == FIBER       worst case: FIBER -> 1     best case: FIBER -> 0
            # row[3] == SNR         worst case:   SNR -> ?     best case: SNR   -> infinity
            # row[4] == BW          worst case:    BW -> ?     best case: BW    -> 1536000
            meanBER = A * row[1] + (1 - A) * meanBER
            meanSNR = A * row[3] + (1 - A) * meanSNR
            
            if (meanBER < thresholdBER and (mySimpleMathLib.ABS(row[4] - 1536000) <= thresholdBW)):
                if (meanSNR < thresholdSNR and row[4] > 0.95):
                    # Impossible but count as error anyway
                    error += 1
            else:
                if row[4] != 0:
                    # Bad Signal
                    error += 1

            # 2-at all              0-not at all
            # good BER? | good SNR? | good FIBER? | good BW?  | Description                                 error
            #     1     |     1     |     2       |     1     | Ideal Signal                                0
            #     1     |     1     |     1       |     1     | Good enough Signal                          0
            #     1     |     1     |     0       |     1     | ... (invalid thresholdBER)                  0

            #     1     |     0     |     2       |     1     | Weak Signal but not an error                0
            #     1     |     0     |     1       |     1     | Weak Signal but not an error                0
            #     1     |     0     |     0       |     1     | ... (impossible)                            1

            #     0     |     1     |     2       |     1     | ... (invalid thresholdBER)                  0
            #     0     |     1     |     1       |     1     | Bad Signal                                  1
            #     0     |     1     |     0       |     1     | Bad Signal                                  1

            #     0     |     0     |     2       |     1     | ... (invalid thresholds)                    0
            #     0     |     0     |     1       |     1     | Bad Signal                                  1
            #     0     |     0     |     0       |     1     | Bad Signal                                  1
            # if BW is not correct we definitely have a problem !

            if error > thresholdError:
                print("Sending SNMP Trap!")
                sendTrap()
                error = 0
        
        checkProcess()
        # in principle its getLastDateTime() but with safety net
        last_datetime = getLastDateTime()
except Exception:
    print("Welle-cli is not running!")
    print("Note that you have to start SNMPhandler.py again!")
except:
    print("End of SNMPhandler!")
    cursor.close()
    db.close()
