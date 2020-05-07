import MySQLdb
from datetime import datetime           # https://docs.python.org/3/library/datetime.html#module-datetime
from time import sleep

def getDateTime(q):
    cursor.execute("SELECT id, datetime FROM dabtable1 WHERE datetime=(SELECT " + q + "(datetime) FROM dabtable1)")
    # SELECT id, datetime FROM dabtable1 WHERE datetime=(SELECT MAX(datetime) FROM dabtable1);
    db.commit()
    data = cursor.fetchone()     
    if data is not None:
        return data[1]  #type: <datetime.datetime>
    else:
        print("Table is empty!")
        return None

def showData():
    cursor.execute("SELECT * FROM dabtable1")
    db.commit()
    data = cursor.fetchall()
    for row in data:
        print(row)

def StartUp(timeout = 30):
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




StartUp(30)