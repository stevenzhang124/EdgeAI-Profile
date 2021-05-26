import sqlite3

conn = sqlite3.connect('edgedemo.db')
print("Opened database successfully")
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS REID")
print("Delete Table successfully")

c.execute('''CREATE TABLE IF NOT EXISTS REID
	   (PERSON TEXT     NOT NULL,
       CTIME           INT    NOT NULL,
       CAMERA INT);''')
print("Table created successfully")
conn.commit()


conn.close()