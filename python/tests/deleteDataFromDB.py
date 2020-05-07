import MySQLdb
from datetime import datetime

regularlyDeleteDataAfterTime = 30                 # seconds
keepData = 60                                     # seconds

# Connect to DB
try:
    db = MySQLdb.connect(host="localhost", user="stu", passwd="korona2020", db="bakalarka")
    cursor = db.cursor()
except:
    print("Could not connect to database!")
    cursor.close()
    db.close()
    exit()

def getDateTime(q):
    cursor.execute("SELECT id, datetime FROM dabtable1 WHERE datetime=(SELECT " + q + "(datetime) FROM dabtable1)")
    data = cursor.fetchone()     
    if data is not None:
        return data[1]  #datetime.datetime
    else:
        print("Table is empty!")
        return None

def deleteData(keeping_data, newestDateTimeOfData):
    """Deletes data that are older than given seconds <float> relative to the given datetime of newest data."""
    delta = newestDateTimeOfData.timestamp() - keeping_data
    delta = datetime.fromtimestamp(delta).strftime('%Y-%m-%d %H-%M-%S')
    cursor.execute("DELETE FROM dabtable1 WHERE datetime < '" + delta + "'")
    cursor.execute("DELETE FROM dabtable2 WHERE datetime < '" + delta + "'")
    cursor.execute("DELETE FROM temperature WHERE datetime < '" + delta + "'")
    db.commit()

def showData():
    cursor.execute("SELECT * FROM dabtable1")
    db.commit()
    data = cursor.fetchall()
    for row in data:
        print(row)


newest_data = getDateTime("MAX")
N = keepData + 1 + regularlyDeleteDataAfterTime
if N > keepData + regularlyDeleteDataAfterTime:
    # We have more data than we want to keep
    oldestDateTimeOfData = getDateTime("MIN")
    print(oldestDateTimeOfData)
    if newest_data.timestamp() - oldestDateTimeOfData.timestamp() > keepData:
        # Making sure we have more data than we want to keep
        N = keepData
        deleteData(keepData, newest_data)


showData()

cursor.close()
db.close()