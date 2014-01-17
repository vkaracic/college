#### Projekt iz Upravljanja znanjem u razvoju programske podrške

Zadatak je napraviti programsku podršku za robota koja ga vodi od točke A do točke B (cilja). Robot je model Lego NXT i opremljen se senzorima za dodir, boju i ultrazvukom, te kreće se pomoću aktuatora. Jedan korak je fiksiran na 30 cm a rotacija na 90*x stupnjeva okreta, gdje je x broj okretaja.
Smješten je u svijetu koji je diskretiziran i podjeljen u polja dimenzija 30x30 cm koje su podjeljene na prohodna polja, prepreke i cilj. Prepreke su dalje podjeljene na zidove i rupe. 

Robot prvo istražuje svijet po algoritmu opisanom u istrazivac.cmap. Svakom polju dodjeluje koordinate i težine (prohodnom 0.5, prepreci 9999 u tablici (bazi?) za najkraći put; a prohodnom minimalno 1 i prepreci minimalno 9999 u tablici polja pri istraživanju). 

Nakon što istraživač istraži čitav svijet, trebalo bi (*nadam se*) biti moguće postaviti robot i cilj na bilo koje koordinate te bi se mogao izračunati najkraći put prije nego što se robot pokrene. 
