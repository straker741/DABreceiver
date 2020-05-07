#!/usr/bin/python3
# Autor: Jakub Svajka
# Date:  7.5.2020

import MySQLdb
from datetime import datetime           # https://docs.python.org/3/library/datetime.html#module-datetime
from time import sleep
import subprocess
import mySimpleMathLib
import SNMPhandler

# ----------------- CONSTANTS ----------------- #
A = 0.1
thresholdBER = 0.2
thresholdSNR = 5
thresholdError = 10
thresholdBW = 1000
numberOfEntriesWeWantToDelete = 3600*24*7        # seconds
numberOfEntriesWeWantToKeep = 3600*24*30*6                         # seconds

core_q  = "SELECT t1.id, t1.BER AS BER, t1.FIBER AS FIBER, t2.SNR AS SNR, t2.bandwidth AS BW, t1.datetime "
core_q += "FROM dabtable1 AS t1 "
core_q += "JOIN dabtable2 AS t2 ON t1.datetime = t2.datetime "

# ----------------- FUNCTIONS ----------------- #
def getDateTime(q):
    cursor.execute("SELECT id, datetime FROM dabtable1 WHERE datetime=(SELECT " + q + "(datetime) FROM dabtable1)")
    db.commit()
    data = cursor.fetchone()     
    if data is not None:
        return data[1]  #type: <datetime.datetime>
    else:
        print("Table is empty!")
        return None

def init(timeout = 30):
    """At Start table may be empty, or receiver is not adjusted and needs some time."""
    
    last_dt = getDateTime("MAX")
    # Firstly, wait for some data to be inserted in case we are starting the script for the very first time when the table is empty
    while last_dt == None:
        # if last_dt == None => Table is empty!
        print("Database is empty!")
        print("Waiting for new data.")
        sleep(3)                   # wait for a while
        last_dt = getDateTime("MAX")
    
    # Secodly, check whether new data are continuosly flowing into the table
    while True:
        sleep(3)     # wait for a while
        if last_dt.timestamp() < getDateTime("MAX").timestamp():
            break
        else:
            print("Waiting for new data.")

    # table is not empty anymore and data are continuosly flowing!
    # Give the receiver some time to adjust
    sleep(timeout)
    print("Ending Initialization!")
    return None

def checkProcess(prc):
    """Starts Bash command and checks whether that process is running."""
    # Note that when starting process ps fx, total 3 and more processes are found
    p = subprocess.Popen("ps fx | grep " + prc, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    out = p.communicate()[0].splitlines()
    if len(out) < 3:
        # Process is not running
        return False
    else:
        return True

def checkWelle():
    """Check how many processes with name welle-cli are running."""
    if not checkProcess("welle-cli"):
        print("Welle-cli is not running!")
        print("Note that you have to start evaluation.py again!")
        cursor.close()
        db.close()
        exit()
    else:
        print("Welle-cli is running. OK!")
    return None

def deleteData(numberOfEntriesWeWantToKeep, newestDateTimeOfData):
    """Deletes data that are older than given seconds <float> relative to the given datetime of newest data."""
    delta = newestDateTimeOfData.timestamp() - numberOfEntriesWeWantToKeep
    delta = datetime.fromtimestamp(delta).strftime('%Y-%m-%d %H-%M-%S')
    print("DELETING DATA OLDER THAN", delta)
    cursor.execute("DELETE FROM dabtable1 WHERE datetime < '" + delta + "'")
    cursor.execute("DELETE FROM dabtable2 WHERE datetime < '" + delta + "'")
    cursor.execute("DELETE FROM temperature WHERE datetime < '" + delta + "'")
    db.commit()
    return None

# Connect to DB
try:
    db = MySQLdb.connect(host="localhost", user="stu", passwd="korona2020", db="bakalarka")
    cursor = db.cursor()
except:
    print("Could not connect to database!")
    cursor.close()
    db.close()
    exit()
print("Successfully connected to database. OK!")

# Check whether welle-cli is running
checkWelle()    
init(30)
# Check whether welle-cli is still running
checkWelle()

newestDateTimeOfData = getDateTime("MAX")
sleep(3)

meanBER = 0
meanSNR = 0
error = 0
N = 0
showQuery = True
try:
    # Main never-ending loop 
    while True:
        dt = newestDateTimeOfData.strftime('%Y-%m-%d %H-%M-%S')
        q = core_q + "WHERE t1.datetime > '" + dt + "'"
        if showQuery:
            print(q)
            showQuery = False
        cursor.execute(q)
        db.commit()
        data = cursor.fetchall()

        # Evaluate Data and decide whether to send SNMP Trap !
        for row in data:
            print(row)
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
            
            if error > thresholdError:
                print("Sending SNMP Trap!")
                SNMPhandler.sendTrap()
                error = 0
            

        # DELETE DATA FROM DB AFTER SOME TIME !!!
        N += len(data)
        if N > (numberOfEntriesWeWantToKeep + numberOfEntriesWeWantToDelete):
            # We have more data than we want to keep
            oldestDateTimeOfData = getDateTime("MIN")
            if newestDateTimeOfData.timestamp() - oldestDateTimeOfData.timestamp() > numberOfEntriesWeWantToKeep:
                # Making sure we have more data than we want to keep
                N = numberOfEntriesWeWantToKeep
                deleteData(numberOfEntriesWeWantToKeep, newestDateTimeOfData)

        checkWelle()
        sleep(5)

        if data:
            newestDateTimeOfData = data[-1][5]
except KeyboardInterrupt:
    print("End of evaluation!")
cursor.close()
db.close()

# Principle of evaluation
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