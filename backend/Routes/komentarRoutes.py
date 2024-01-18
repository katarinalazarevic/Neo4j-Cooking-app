from datetime import datetime
from json import dumps
from flask import request,jsonify, Blueprint
from py2neo import Graph, Node
from bcrypt import checkpw, hashpw, gensalt
from database import graph

komentar_routes = Blueprint("komentar_routes", __name__)

@komentar_routes.route('/dodajKomentar',methods=['POST'])
def dodajKomentar():
    try:
        data=request.get_json()
        korisnik_email=data.get("korisnik_email")
        sadrzaj=data.get("sadrzaj")
        datum=datetime.now()

        komentar=Node("Komentar",sadrzaj=sadrzaj,datum_postavljanja=datum)
        graph.create(komentar)
        korisnik = graph.run("MATCH (k:Korisnik {email: $email}) RETURN k", email=korisnik_email).evaluate()
        if not korisnik:
            return "Korisnik sa datim email-om ne postoji."

        naziv_recepta = data.get("naziv_recepta")
        recept = graph.run("MATCH (r:Recept {naziv: $naziv}) RETURN r", naziv=naziv_recepta).evaluate()

        if not recept:
            return "Recept sa datim nazivom ne postoji."

        # Poveži korisnika sa receptom kroz komentar
        povezi_query = "MATCH (k:Korisnik {email: $email}), (r:Recept {naziv: $naziv}), (kom:Komentar {sadrzaj:$sadrzaj}) " \
                       "CREATE (k)-[:OSTAVLJA]->(kom)-[:ZA]->(r)"
        graph.run(povezi_query, email=korisnik_email, naziv=naziv_recepta,sadrzaj=sadrzaj)

        return "Komentar uspešno dodat."
    
    except Exception as e:
        return str(e), 500  # 500 označava internu serversku grešku

from py2neo import Node, Relationship

@komentar_routes.route('/obrisiKomentar', methods=["DELETE"])
def obrisiKomentar():
    try:
        data = request.get_json()
        sadrzaj = data.get("sadrzaj")
        rec=graph.run("MATCH (r:Komentar {sadrzaj: $sadrzaj}) DETACH DELETE r", sadrzaj=sadrzaj)
        return "Komentar uspešno obrisan."

    except Exception as e:
        return f"Greška prilikom brisanja komentara: {str(e)}", 500

@komentar_routes.route('/izmeniKomentar', methods=["PUT"])
def izmeniKomentar():
    try:
        data = request.get_json()
        stari_sadrazaj = data.get("sadrzaj")
        novi_sadrzaj = data.get("novi_sadrzaj")
        
        # Provera da li komentar postoji
        existing_komentar = graph.run("MATCH (k:Komentar {sadrzaj: $sadrzaj}) RETURN k", sadrzaj=stari_sadrazaj)
        existing_komentar = existing_komentar.evaluate()

        if not existing_komentar:
            return "Komentar sa datim ID-om ne postoji."

        # Ažuriranje sadržaja komentara
        graph.run("MATCH (k:Komentar {sadrzaj: $sadrzaj}) SET k.sadrzaj = $novi_sadrzaj", sadrzaj=stari_sadrazaj, novi_sadrzaj=novi_sadrzaj)

        return "Komentar uspešno izmenjen."

    except Exception as e:
        return f"Greška prilikom izmene komentara: {str(e)}", 500
    
@komentar_routes.route('/komentariKorisnika', methods=["POST"])
def komentariKorisnika():
    try:
        data = request.get_json()
        korisnik_email = data.get("korisnik_email")
        print(korisnik_email)
        # Dohvatanje svih komentara koje je postavio određeni korisnik
        result = graph.run("MATCH (k:Korisnik {email: $korisnik_email})-[:OSTAVLJA]->(kom:Komentar)-[:ZA]->(r:Recept) RETURN kom, r", korisnik_email=korisnik_email)
        komentari = [record["kom"]["sadrzaj"] for record in result]

        # Vraćamo rezultat u JSON formatu
        return dumps({"komentari": komentari}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return f"Greška prilikom dohvatanja komentara korisnika: {str(e)}", 500
@komentar_routes.route('/komentariZaRecept', methods=["POST"])
def komentariZaRecept():
    try:
        data = request.get_json()
        naziv_recepta = data.get("naziv_recepta")

        query = """
        MATCH (r:Recept {naziv: $naziv_recepta})<-[:ZA]-(k:Komentar)<-[:OSTAVLJA]-(korisnik:Korisnik)
        WITH k, korisnik
        RETURN k.sadrzaj AS sadrzaj_komentara, korisnik.email AS email_korisnika
        """

        result = graph.run(query, naziv_recepta=naziv_recepta)
        komentari = [{"sadrzaj": record["sadrzaj_komentara"], "korisnik_email": record["email_korisnika"]} for record in result]

        return jsonify({"komentari": komentari})

    except Exception as e:
        return str(e), 500
