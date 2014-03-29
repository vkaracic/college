import MySQLdb
import NNlib

# Konekcija na bazu
conn = MySQLdb.connect(host="localhost", user="root", passwd="lozinka", db="istrazivac")
cursor = conn.cursor()

# POCETAK
cursor.execute("CALL init")
conn.commit()

# Petlja koje se stalno vrti dok korisnik ne unese broj
while True:
    # Ucitaj trenutne koordinate
    cursor.execute("SELECT xkoord, ykoord FROM polje WHERE poljeID = (SELECT poljeID FROM stanje)")
    xkoord, ykoord = cursor.fetchone() # spremi rezultate SQL querya u varijable

    # Povecaj tezinu polja na kojem se nalazis za 2
    cursor.execute("CALL povecaj_tezinu(%s, %s)",(xkoord, ykoord))
    conn.commit()

    # U 'okruzenje' se spremaju sva polja okolo robota u tom trenutku da bi se mogalo izracunati sljedece polje na koje ce robot ici. Format: {ID polja: tezina polja}
    okruzenje = dict()

    cursor.execute("SELECT d_tezina FROM polje WHERE poljeID = (SELECT poljeID FROM stanje); ")
    t_tezina = cursor.fetchone()

    # Petlja za skeniranje okolo sebe, 1 - 4 za svaku stranu
    for i in range(4):
        # Skeniraj senzorima polje ispred sebe
        # - rucni unos vrijednosti senzora
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
        cursor.execute("SELECT smjer, poljeID FROM stanje;")
        smjer, t_polje = cursor.fetchone()
        # - izracunaj i spremi vrijednosti polja ispred
        cursor.execute("CALL spremi_polje_ispred(%s)", smjer)

        # - dodaj vrijednosti polja u okruzenje
        cursor.execute("SELECT poljeID, tezina, d_tezina FROM polje WHERE xkoord = @pi_x AND ykoord = @pi_y")
        poljeID, tezina, d_tezina= cursor.fetchone()
        okruzenje[int(poljeID)] = int(tezina)

        cursor.execute("CALL dodajVezu('%s','veza', '%s', %s);", (t_polje, poljeID, d_tezina))
        conn.commit()

        # - ucitaj koordinate polja ispred
        cursor.execute("SELECT @pi_x, @pi_y;")
        pi_x, pi_y = cursor.fetchone()
        # - spremi t_smjer vrijednost polja ispred
        cursor.execute("UPDATE polje SET t_smjer = (SELECT smjer FROM stanje) WHERE xkoord = %s AND ykoord = %s;", (pi_x, pi_y))
        conn.commit()

        # - izvjestaj korisniku sto je spremljeno u bazu (manualna kontrola tocnosti)
        print "%s spremljeno na polju (%s, %s)" % (koncept, pi_x, pi_y)
        # Skreni 90 stupnjeva na desno; smjeru se dodaje +90, a ako je vece od 250 vraca se na 0
        cursor.execute("UPDATE stanje SET smjer = IF(smjer < 250, smjer + 90, 0);")
        conn.commit()
        print "Okrecem se desno 90 stupnjeva\n"

    # Izracun sljedeceg polja tako sto se iterira rjecnik 'okruzenje' i uzima kljuc s najmanjom vrijednosti
    s_polje = min(okruzenje, key=okruzenje.get)

    # Idi na sljedece polje s najmanjom tezinom
    # - iz baze se ucitavaju vrijenosti sljedeceg polja koja ce se kasnije spremiti u tablicu 'stanje'
    cursor.execute("SELECT xkoord, ykoord, tezina, t_smjer FROM polje WHERE poljeID = %s", s_polje)
    s_x, s_y, s_tezina, s_smjer = cursor.fetchone()

    # - izvjestaj korisniku gdje robot ide dalje (x, y)[tezina]
    print "IDEM NA (%s, %s)[%s]" % (s_x, s_y, s_tezina)

    # Azuriranje stanja poslije pomaka robota
    cursor.execute("UPDATE stanje SET poljeID = %s;", s_polje)
    cursor.execute("UPDATE stanje SET smjer = %s;", s_smjer)
    cursor.execute("SET @t_x = %s, @t_y = %s", (s_x, s_y))
    conn.commit()

# Zatvaranje konekcije
conn.close()