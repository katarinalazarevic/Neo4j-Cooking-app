class NutritivnaVrednost:
    def _init_(self, proteini, masti, ugljeni_hidrati, kalorije):
        self.proteini = proteini
        self.masti = masti
        self.ugljeni_hidrati = ugljeni_hidrati
        self.kalorije = kalorije

    def _str_(self):
        return f"Proteini: {self.proteini}g, Masti: {self.masti}g, Ugljeni hidrati: {self.ugljeni_hidrati}g, Kalorije: {self.kalorije}kcal"


# Primer korišćenja
nutritivna_vrednost = NutritivnaVrednost(proteini=25, masti=15, ugljeni_hidrati=30, kalorije=300)

# Prikazivanje nutritivnih vrednosti
print(nutritivna_vrednost)