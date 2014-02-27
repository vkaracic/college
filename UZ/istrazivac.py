import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="lozinka", db="istrazivac")
cursor = conn.cursor()

cursor.execute("CALL init")
conn.commit()

cursor.execute("SELECT xkoord, ykoord FROM polje WHERE poljeID = (SELECT poljeID from stanje)")
xkoord, ykoord = cursor.fetchone()

print xkoord, ykoord
cursor.execute("CALL povecaj_tezinu(%s, %s)",(xkoord, ykoord))
conn.commit()

## Skeniraj senzorima polje ispred sebe
## trebat ce koristiti manualni unos za sada

## Dodati te vrijednosti u bazu:
###   izracunati koordinate polja ispred
###   pogledati ima li vec uneseno polje s tim koordinatama
###     i unijeti koordinate accordingly

## Srenuti robota za 90 stupnjeva u desnu stranu 

## Ponoviti Skeniranje