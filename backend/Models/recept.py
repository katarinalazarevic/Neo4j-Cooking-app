from Models.nutritivnavrednost import NutritivnaVrednost
from Models.sastojak import Sastojak


class Recept:
    def _init_(self, naziv, sastojci):
        self.naziv = naziv
        self.sastojci = sastojci

    def dodaj_sastojak(self, sastojak):
        self.sastojci.append(sastojak)

    def _str_(self):
        return f"Recept: {self.naziv}\nSastojci: {', '.join([str(s) for s in self.sastojci])}"

# Primer korišćenja
nutritivna_vrednost_sira = NutritivnaVrednost(proteini=10, masti=5, ugljeni_hidrati=15, kalorije=150)
sir = Sastojak(ime="Sir", gramaza=200, nutritivna_vrednost=nutritivna_vrednost_sira)

nutritivna_vrednost_testenine = NutritivnaVrednost(proteini=12, masti=2, ugljeni_hidrati=40, kalorije=200)
testenina = Sastojak(ime="Testenina", gramaza=300, nutritivna_vrednost=nutritivna_vrednost_testenine)

recept = Recept(naziv="Pita sa sirom", sastojci=[sir, testenina])

# Prikazivanje informacija o receptu
print(recept)