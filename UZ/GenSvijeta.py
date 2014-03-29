import MySQLdb

# Konekcija na bazu
conn = conn = MySQLdb.connect(host="localhost", user="root", passwd="lozinka", db="istrazivac")
cursor = conn.cursor()

svijet = dict()

cursor.execute("SELECT xkoord, ykoord, d_tezina FROM polje;")
for i in xrange(cursor.rowcount):
    xkoord, ykoord, tezina = cursor.fetchone()
    key = (int(xkoord), int(ykoord))
    svijet[str(key)] = int(tezina)

cursor.execute("DROP TABLE IF EXISTS cvor")
conn.commit()

cursor.execute("CREATE TABLE cvor ")

cursor.execute("DELETE FROM svijet;")
cursor.execute("ALTER TABLE svijet AUTO_INCREMENT = 1;")
conn.commit()

for key, value in svijet.iteritems():
    cursor.execute("INSERT INTO svijet (koord, tezina) VALUES(%s, %s);", (key, value))
    conn.commit()