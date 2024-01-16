class Sastojak:
    def __init__(self, naziv,kalorijska_vrednost,proteini,masti,ugljeni_hidrati,cena):
        self.naziv = naziv
        self.kalorijska_vrednost=kalorijska_vrednost
        self.proteini=proteini
        self.masti=masti
        self.ugljeni_hidrati=ugljeni_hidrati
        self.cena=cena


    def dodaj_sastojak(self):
        # Proveri da li sastojak sa datim nazivom već postoji
        existing_sastojak = self.graph.run("MATCH (s:Sastojak {naziv: $naziv}) RETURN s", naziv=self.naziv).first()

        if existing_sastojak:
            return "Sastojak sa datim nazivom već postoji."

        # Kreiraj novi sastojak
        #sastojak = Node("Sastojak", naziv=self.naziv)
        #self.graph.create(sastojak)

        return "Sastojak uspešno dodat."

    def vrati_sastojke(self):
        # Vrati sve sastojke
        result = self.graph.run("MATCH (s:Sastojak) RETURN s")
        sastojci = [record["s"] for record in result]

        return sastojci
