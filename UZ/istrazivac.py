import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="lozinka", db="istrazivac")
cursor = conn.cursor()

cursor.execute("CALL init")
conn.commit()

poljeID = int(cursor.execute("SELECT poljeID FROM stanje"))
cursor.execute("SELECT xkoord, ykoord FROM polje WHERE poljeID = %s;", poljeID)
xkoord, ykoord = cursor.fetchone()

print xkoord, ykoord
# cursor.execute("CALL povecaj_tezinu(")
# conn.commit()