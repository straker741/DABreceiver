# Autor: Jakub Svajka
# Date:  14.4.2020

import MySQLdb
import time

# ----------------- CONSTANTS ----------------- #
A = 0.1
thresholdBER = 0.2
thresholdSNR = 5
thresholdError = 10

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
        print("Database is empty!")
        cursor.close()
        db.close()
        exit()

def sendTrap():
    pass

try:
    db = MySQLdb.connect(host="localhost", user="stu", passwd="korona2020", db="bakalarka")
    cursor = db.cursor()

    # Firstly, get last_datetime
    last_datetime = getLastDateTime()

    # Secodly, check whether new data are flowing into the database
    while True
        time.sleep(1.5)     # wait for a while
        if last_datetime < getLastDateTime():
            break
        else:
            print("Waiting for new data.")


    meanBER = 0
    meanSNR = 0
    meanFIBER = 0
    error = 0
    # Main loop 
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
            
            if meanBER < thresholdBER:
                if (meanSNR < thresholdSNR and row[4] > 0.95):
                    # Impossible but count as error anyway
                    error += 1
            else:
                if row[4] != 0:
                    # Bad Signal
                    error += 1

            # 2-at all              0-not at all
            # good BER? | good SNR? | good FIBER? | Description                                 error
            #     1     |     1     |     2       | Ideal Signal                                0
            #     1     |     1     |     1       | Good enough Signal                          0
            #     1     |     1     |     0       | ... (invalid thresholdBER)                  0

            #     1     |     0     |     2       | Weak Signal but not an error                0
            #     1     |     0     |     1       | Weak Signal but not an error                0
            #     1     |     0     |     0       | ... (impossible)                            1

            #     0     |     1     |     2       | ... (invalid thresholdBER)                  0
            #     0     |     1     |     1       | Bad Signal                                  1
            #     0     |     1     |     0       | Bad Signal                                  1

            #     0     |     0     |     2       | ... (invalid thresholds)                    0
            #     0     |     0     |     1       | Bad Signal                                  1
            #     0     |     0     |     0       | Bad Signal                                  1

            if error > thresholdError:
                print("Sending SNMP Trap!")
                sendTrap()
                error = 0
        last_datetime = getLastDateTime()
except KeyboardInterrupt:
    print("End of SNMPhandler!")
except:
    print("Could not connect to database!")
cursor.close()
db.close()
