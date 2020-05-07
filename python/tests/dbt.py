import MySQLdb

q = "SELECT t1.id, t1.BER AS BER, t1.FIBER AS FIBER, t2.SNR AS SNR, t2.bandwidth AS BW, t1.datetime FROM dabtable1 AS t1 JOIN dabtable2 AS t2 ON t1.datetime = t2.datetime WHERE t1.datetime > '2020-05-07 16-40-19'"

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


cursor.execute(q)
db.commit()
data = cursor.fetchall()

for row in data:
    print(row)
