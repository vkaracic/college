import MySQLdb
import NNlib

# konekcija na bazu
conn = MySQLdb.connect(host="localhost", user="root", passwd="lozinka", db="istrazivac")
cursor = conn.cursor()

# POCETAK
cursor.execute("CALL init")
conn.commit()
while True:
    # Ucitaj trenutne koordinate
    cursor.execute("SELECT xkoord, ykoord FROM polje WHERE poljeID = (SELECT poljeID from stanje)")
    xkoord, ykoord = cursor.fetchone()

    # Povecaj tezinu polja na kojem se nalazis za 1
    cursor.execute("CALL povecaj_tezinu(%s, %s)",(xkoord, ykoord))
    conn.commit()

    # Skeniraj senzorima polje ispred sebe
    # - rucni unos vrijednosti senzora

    for i in range(4):
        print "Unesi vrijednosti za polje ispred"
        SB = input("SB: ")
        UZ = input("UZ: ")

        # - odredjivanje koncepta na osnovu vrijednosti koje NN vrati
        if NNlib.neuro(SB, UZ) == 1:
            koncept = 'zid'
        else:
            koncept = 'prazan prostor'

        # - ucitaj koji je koncept u varijablu
        sql = "SET @koncept:='%s';" % koncept
        cursor.execute(sql)
        conn.commit()

        # Dodaj vrijednosti i koordinate u bazu
        # - ucitavanje trenutnog smjera za izracun koordinata polja ispred
        cursor.execute("SELECT smjer FROM stanje;")
        smjer = cursor.fetchone()
        # - izracunaj i spremi vrijednosti polja ispred
        cursor.execute("CALL spremi_polje_ispred(%s)", smjer)

        # - ucitaj koordinate polja ispred
        cursor.execute("SELECT @pi_x, @pi_y;")
        pi_x, pi_y = cursor.fetchone()
        # - spremi t_smjer vrijednost polja ispred
        cursor.execute("UPDATE polje SET t_smjer = (SELECT smjer FROM stanje) WHERE xkoord = %s AND ykoord = %s;", (pi_x, pi_y))
        conn.commit()


        print "%s spremljeno na polju (%s, %s)\n" % (koncept, pi_x, pi_y)
        # Skreni 90 stupnjeva na desno
        cursor.execute("UPDATE stanje SET smjer = IF(smjer < 250, smjer + 90, 0);")
        conn.commit()
        print "Okrecem se desno 90 stupnjeva"

    # Idi na sljedece polje s najmanjom tezinom
    cursor.execute("CALL sljedece_polje()")
    cursor.execute("SELECT @s_polje;")
    s_polje = cursor.fetchone()

    cursor.execute("SELECT xkoord, ykoord, tezina, t_smjer FROM polje WHERE poljeID = %s", s_polje)
    s_x, s_y, s_tezina, s_smjer = cursor.fetchone()
    print "Idem na sljedece polje (%s, %s)[%s]" % (s_x, s_y, s_tezina)

    # Azuriranje stanja poslije pomaka robota
    cursor.execute("UPDATE stanje SET poljeID = %s;", s_polje)
    cursor.execute("UPDATE stanje SET smjer = %s;", s_smjer)
    conn.commit()
conn.close()

## +Skeniraj senzorima polje ispred sebe
## +trebat ce koristiti manualni unos za sada

## Dodati te vrijednosti u bazu:
###   izracunati koordinate polja ispred
###   pogledati ima li vec uneseno polje s tim koordinatama
###     i unijeti koordinate accordingly

## Srenuti robota za 90 stupnjeva u desnu stranu 

## Ponoviti Skeniranje