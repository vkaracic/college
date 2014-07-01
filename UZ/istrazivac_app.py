from PySide.QtCore import *
from PySide.QtGui import *
import sys
import MySQLdb
import NNlib

import crtanjeSvijeta

class Prozor(QWidget):
    def __init__(self):
        super(Prozor, self).__init__()
        self.brojac = 0

        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="lozinka", db="istrazivac")
        self.cursor = self.conn.cursor()

        # POCETAK
        self.cursor.execute("CALL init")
        self.conn.commit()

        

        self.okruzenje = dict()



        SBLabel = QLabel("SB: ")
        UZLabel = QLabel("UZ: ")
        self.SBSpinBox = QSpinBox()
        self.UZSpinBox = QSpinBox()
        unesiButton = QPushButton("Unesi")
        self.unesenaVrijednost = QLabel()
        self.promjenaPozicije= QLabel()
        self.pokret = QLabel()
        krajButton = QPushButton("Kraj")

        layout = QGridLayout()
        layout.addWidget(SBLabel, 0, 0)
        layout.addWidget(self.SBSpinBox, 0, 1)
        layout.addWidget(UZLabel, 0, 2)
        layout.addWidget(self.UZSpinBox, 0, 3)
        layout.addWidget(unesiButton, 0, 4)

        layout.addWidget(self.unesenaVrijednost, 1, 0, 1, 4)
        layout.addWidget(self.promjenaPozicije, 2, 0, 1, 4)
        layout.addWidget(self.pokret, 3, 0, 1, 4)

        layout.addWidget(krajButton, 4, 0)

        self.setLayout(layout)

        self.connect(unesiButton, SIGNAL("clicked()"), self.istrazuj)
        self.connect(krajButton, SIGNAL("clicked()"), self.kraj)


    def istrazuj(self):

        SB = self.SBSpinBox.value()
        UZ = self.UZSpinBox.value()

        # - odredjivanje koncepta na osnovu vrijednosti koje NN vrati
        if NNlib.neuro(SB, UZ) == 1:
            koncept = 'zid'
        else:
            koncept = 'prazan prostor'

        # - ucitaj koji je koncept u varijablu
        sql = "SET @koncept:='%s';" % koncept
        self.cursor.execute(sql)
        self.conn.commit()

        # Dodaj vrijednosti i koordinate u bazu
        # - ucitavanje trenutnog smjera za izracun koordinata polja ispred
        self.cursor.execute("SELECT smjer, poljeID FROM stanje;")
        smjer, t_polje = self.cursor.fetchone()
        # - izracunaj i spremi vrijednosti polja ispred
        self.cursor.execute("CALL spremi_polje_ispred(%s)", smjer)

        # - dodaj vrijednosti polja u okruzenje
        self.cursor.execute("SELECT poljeID, tezina, d_tezina FROM polje WHERE xkoord = @pi_x AND ykoord = @pi_y")
        poljeID, tezina, d_tezina= self.cursor.fetchone()
        self.okruzenje[int(poljeID)] = int(tezina)

        self.cursor.execute("CALL dodajVezu('%s','veza', '%s', %s);", (t_polje, poljeID, d_tezina))
        self.conn.commit()

        # - ucitaj koordinate polja ispred
        self.cursor.execute("SELECT @pi_x, @pi_y;")
        pi_x, pi_y = self.cursor.fetchone()
        # - spremi t_smjer vrijednost polja ispred
        self.cursor.execute("UPDATE polje SET t_smjer = (SELECT smjer FROM stanje) WHERE xkoord = %s AND ykoord = %s;", (pi_x, pi_y))
        self.conn.commit()
        self.unesenaVrijednost.setText(("<font color='green'>%s spremljeno na polju (%s, %s)</font>") % (koncept, pi_x, pi_y))
        self.promjenaPozicije.setText("<font color='green'>Okrecem se desno 90 stupnjeva</font>")
        # Skreni 90 stupnjeva na desno; smjeru se dodaje +90, a ako je vece od 250 vraca se na 0
        self.cursor.execute("UPDATE stanje SET smjer = IF(smjer < 250, smjer + 90, 0);")
        self.conn.commit()

        self.brojac += 1
        if self.brojac == 4:
            self.brojac = 0
            self.master_istrazuj()

    def master_istrazuj(self):
        s_polje = min(self.okruzenje, key=self.okruzenje.get)

        # Idi na sljedece polje s najmanjom tezinom
        # - iz baze se ucitavaju vrijenosti sljedeceg polja koja ce se kasnije spremiti u tablicu 'stanje'
        self.cursor.execute("SELECT xkoord, ykoord, tezina, t_smjer FROM polje WHERE poljeID = %s", s_polje)
        s_x, s_y, s_tezina, s_smjer = self.cursor.fetchone()

        # - izvjestaj korisniku gdje robot ide dalje (x, y)[tezina]
        self.pokret.setText(("<font color='green'>IDEM NA (%s, %s)[%s]</font>") % (s_x, s_y, s_tezina))

        # Azuriranje stanja poslije pomaka robota
        self.cursor.execute("UPDATE stanje SET poljeID = %s;", s_polje)
        self.cursor.execute("UPDATE stanje SET smjer = %s;", s_smjer)
        self.cursor.execute("SET @t_x = %s, @t_y = %s", (s_x, s_y))
        self.conn.commit()

        self.cursor.execute("SELECT xkoord, ykoord FROM polje WHERE poljeID = (SELECT poljeID FROM stanje)")
        xkoord, ykoord = self.cursor.fetchone() # spremi rezultate SQL querya u varijable

        # Povecaj tezinu polja na kojem se nalazis za 2
        self.cursor.execute("CALL povecaj_tezinu(%s, %s)",(xkoord, ykoord))
        self.conn.commit()

        # U 'okruzenje' se spremaju sva polja okolo robota u tom trenutku da bi se mogalo izracunati sljedece polje na koje ce robot ici. Format: {ID polja: tezina polja}
        self.okruzenje = dict()


    def kraj(self):
        crtanjeSvijeta.main()



app = QApplication(sys.argv)
form = Prozor()
form.show()
app.exec_()