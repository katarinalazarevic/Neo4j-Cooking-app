from flask import request,jsonify, Blueprint
from py2neo import Graph, Node
from bcrypt import checkpw, hashpw, gensalt
from Models.korisnik import Korisnik
from database import graph
recept_routes = Blueprint("recept_routes", __name__)

@recept_routes.route('/dodajRecept',methods=["POST"])
def dodajRecept():
    data=request.get_data()
    naziv=data.get("naziv")
    opis=data.get("opis")
    sastojci=data.get("sastojci")
    korisnik_email=data.get("email")
    korisnik = graph.run("MATCH (k:Korisnik {email: $email}) RETURN k", email=korisnik_email)
    korisnik=korisnik.evaluate()


    if not korisnik:
        return "Korisnik sa datim email-om ne postoji."
    # Kreiraj novi recept
    recept = Node("Recept", naziv=naziv, sastojci=sastojci, opis_pripreme=opis)
    graph.create(recept)
    korisnik_node = korisnik.get("k")
    povezi_query = "MATCH (k:Korisnik {email: $email}), (r:Recept {naziv: $naziv}) " \
                   "CREATE (k)-[:POSTAVLJA]->(r)"
    graph.run(povezi_query, email=korisnik_email, naziv=naziv)
    # Poveži recept sa sastojcima
    for sastojak in sastojci:
        sastojak_node = graph.run("MATCH (s:Sastojak {naziv: $naziv}) RETURN s", naziv=sastojak)
        sastojak_node=sastojak_node.evaluate()
        if not sastojak_node:
            return f"Sastojak '{sastojak}' ne postoji."
        povezi_query = "MATCH (r:Recept {naziv: $naziv}), (s:Sastojak {naziv: $sastojak}) " \
                       "CREATE (r)-[:SADRZI]->(s)"
        graph.run(povezi_query, naziv=naziv, sastojak=sastojak)
    return "Recept uspešno dodat sa sastojcima."
