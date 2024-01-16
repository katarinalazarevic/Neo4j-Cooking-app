from py2neo import Graph, Node
from database import graph

class Korisnik:
    def __init__(self, ime, prezime, datum_rodjenja, email,sifra):
        self.ime = ime
        self.prezime = prezime
        self.datum_rodjenja = datum_rodjenja
        self.email = email
        self.sifra=sifra
    