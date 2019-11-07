import mysql.connector
from mysql.connector import Error
#from sqlite3.test.factory import MyCursor
BD_nombre = 'apdif'

mydb = mysql.connector.connect(host='192.168.100.9',
                                             database= BD_nombre,
                                             user='apdif',
                                             password='TZaJsYQqMjY1lHOK')

MyCursor = mydb.cursor()
#MyCursor.execute("select * from mplb")
MyCursor.execute("USE {}".format(BD_nombre))
MyCursor.execute("SHOW TABLES")
records = MyCursor.fetchall()
#records = MyCursor.fetchall()
for row in records:
    print("id = ", row[0], )
    print("titulo = ", row[1])
    print("referer  = ", row[2])
    print("infringe  = ", row[3], "\n")