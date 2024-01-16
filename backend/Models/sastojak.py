from Models.nutritivnavrednost import NutritivnaVrednost


class Sastojak:
    def _init_(self, ime, gramaza, nutritivna_vrednost):
        self.ime = ime
        self.gramaza = gramaza
        self.nutritivna_vrednost = nutritivna_vrednost

    def _str_(self):
        return f"Ime: {self.ime}, Gramaza: {self.gramaza}g, Nutritivna vrednost: {self.nutritivna_vrednost}"

# Primer korišćenja
nutritivna_vrednost_sastojka = NutritivnaVrednost(proteini=10, masti=5, ugljeni_hidrati=15, kalorije=150)
sastojak = Sastojak(ime="Sir", gramaza=200, nutritivna_vrednost=nutritivna_vrednost_sastojka)

# Prikazivanje informacija o sastojku
print(sastojak)