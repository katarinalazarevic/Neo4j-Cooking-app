from flask import request,jsonify, Blueprint
from py2neo import Graph, Node
from bcrypt import checkpw, hashpw, gensalt
from Models.korisnik import Korisnik
from database import graph
recept_routes = Blueprint("recept_routes", __name__)

@recept_routes.route('/dodajRecept', methods=["POST"])
def dodajRecept():
    data = request.get_json()
    naziv = data.get("naziv")
    opis = data.get("opis_pripreme")
    sastojci = data.get("sastojci")
    kategorija = data.get("kategorija")
    korisnik_email = data.get("email")

    # Proveri da li već postoji recept sa istim nazivom
    existing_recept = graph.run("MATCH (r:Recept {naziv: $naziv}) RETURN r", naziv=naziv)
    existing_recept = existing_recept.evaluate()

    if existing_recept:
        return "Recept sa datim nazivom već postoji."

    # Kreiraj novi recept
    recept = Node("Recept", naziv=naziv, sastojci=sastojci, opis_pripreme=opis, kategorija=kategorija, ocena=0)
    graph.create(recept)

    # Poveži korisnika sa receptom
    povezi_query = "MATCH (k:Korisnik {email: $email}), (r:Recept {naziv: $naziv}) " \
                   "CREATE (k)-[:POSTAVLJA]->(r)"
    graph.run(povezi_query, email=korisnik_email, naziv=naziv)

    # Poveži recept sa sastojcima
    for sastojak in sastojci:
        sastojak_node = graph.run("MERGE (s:Sastojak {naziv: $naziv}) RETURN s", naziv=sastojak).evaluate()

        if not sastojak_node:
            return f"Sastojak '{sastojak}' ne postoji."

        povezi_query = "MATCH (r:Recept {naziv: $naziv}), (s:Sastojak {naziv: $sastojak}) " \
                       "CREATE (r)-[:SADRZI]->(s)"
        graph.run(povezi_query, naziv=naziv, sastojak=sastojak)

    return "Recept uspešno dodat sa sastojcima."


@recept_routes.route('/obrisiRecept', methods=["DELETE"])
def obrisiRecept():
    try:
        data = request.get_json()
        naziv = data.get("naziv")

        # Obriši recept zajedno sa svim vezama i sastojcima
        rec=graph.run("MATCH (r:Recept {naziv: $naziv}) DETACH DELETE r", naziv=naziv)
        rec=rec.evaluate()
        
        return "Recept uspešno obrisan.", 201
    except Exception as e:
        return str(e), 500
    
@recept_routes.route('/azurirajRecept', methods=["POST"])
def azurirajRecept():
    try:
        data = request.get_json()
        stari_naziv = data.get("naziv")
        novi_naziv = data.get("novi_naziv")
        opis = data.get("opis_pripreme")
        sastojci = data.get("sastojci")
        kategorija = data.get("kategorija")
        korisnik_email = data.get("email")

        # Proveri da li recept sa starim nazivom postoji
        stari_recept = graph.run("MATCH (r:Recept {naziv: $naziv}) RETURN r", naziv=stari_naziv)
        stari_recept = stari_recept.evaluate()

        # if not stari_recept:
        #     return f"Recept sa nazivom '{stari_naziv}' ne postoji.", 404

        # Obrisi stare sastojke recepta
        graph.run("MATCH (r:Recept {naziv: $naziv})-[s:SADRZI]->(sastojak:Sastojak) DELETE s", naziv=stari_naziv)
        if(novi_naziv is None):
            novi_naziv=stari_naziv
        # Ažuriraj recept
        graph.run("MATCH (r:Recept {naziv: $stari_naziv}) "
                  "SET r.naziv = $novi_naziv, r.opis_pripreme = $opis, r.sastojci = $sastojci, r.kategorija = $kategorija",
                  stari_naziv=stari_naziv, novi_naziv=novi_naziv, opis_pripreme=opis, sastojci=sastojci, kategorija=kategorija)

        # Dodaj nove sastojke receptu
        for sastojak in sastojci:
            graph.run("MATCH (r:Recept {naziv: $novi_naziv}), (s:Sastojak {naziv: $sastojak}) "
                      "CREATE (r)-[:SADRZI]->(s)", novi_naziv=novi_naziv, sastojak=sastojak)

        return "Recept uspešno ažuriran.", 200
    except Exception as e:
        return str(e), 500

    
@recept_routes.route('/receptiKorisnika', methods=["POST"])
def receptiKorisnika():
    try:
        data=request.get_json()
        email=data.get("email")
        # Pronađi korisnika sa datim email-om
        korisnik = graph.run("MATCH (k:Korisnik {email: $email}) RETURN k", email=email)
        korisnik = korisnik.evaluate()

        if not korisnik:
            return "Korisnik sa datim email-om ne postoji.", 404

        # Pronađi sve recepte koje je korisnik postavio
        result = graph.run("MATCH (k:Korisnik {email: $email})-[:POSTAVLJA]->(r:Recept) RETURN r", email=email)
        recepti = [record["r"] for record in result]

        return jsonify({"recepti": recepti}), 200
    except Exception as e:
        return str(e), 500

@recept_routes.route('/receptiPoKategoriji')
def recepti_po_kategoriji():
    try:
        data=request.get_json()
        kategorija = data.get('kategorija')

        # Pronađi recepte sa datom kategorijom
        result = graph.run("MATCH (r:Recept {kategorija: $kategorija}) RETURN r", kategorija=kategorija)
        recepti = [record["r"] for record in result]

        return jsonify({"recepti": recepti}), 200
    except Exception as e:
        return str(e), 500