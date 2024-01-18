from py2neo import Graph, Node
from database import graph

class Komentar:
    def __init__(self, sadrzaj, datum_postavljanja ):
        self.sadrzaj = sadrzaj
        self.datum_postavljanja = datum_postavljanja
        