import sqlite3
import time

conn = sqlite3.connect('edgedemo.db', isolation_level=None)
print("Opened database successfully")
c = conn.cursor()

p1 = "Person_1"
p2 = "Person_2"
c1 = 1
c2 = 2
c3 = 3

info = "insert into REID (PERSON, CTIME, CAMERA) \
			values ('{}', {}, '{}')".format(p1, int(time.time()), c1)
c.execute(info)

info_1 = "insert into REID (PERSON, CTIME, CAMERA) \
			values ('{}', {}, '{}')".format(p1, int(time.time()), c3)
c.execute(info_1)

info_2 = "insert into REID (PERSON, CTIME, CAMERA) \
			values ('{}', {}, '{}')".format(p1, int(time.time()), c2)
c.execute(info_2)

c.execute("select * from REID")

datas = c.fetchall()
for data in datas:
	print(data)

#c.execute("DROP TABLE REID")
conn.close()	