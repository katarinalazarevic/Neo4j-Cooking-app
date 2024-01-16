from flask import request,jsonify, Blueprint
from py2neo import Graph, Node
from bcrypt import checkpw, hashpw, gensalt
from Models.korisnik import Korisnik
from database import graph
korisnik_routes = Blueprint("korisnik_routes", __name__)

@korisnik_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        ime = data.get("ime")
        prezime = data.get("prezime")
        datum_rodjenja = data.get("datum_rodjenja")
        email = data.get("email")
        sifra=data.get("sifra")

        # Proveri da li korisnik sa istim email-om već postoji
        existing_user = graph.run("MATCH (k:Korisnik {email: $email}) RETURN k", email=email)
    
    # Koristi evaluate() da dobiješ prvi rezultat
        existing_user = existing_user.evaluate()

        if existing_user:
            return "Korisnik već postoji sa ovim email-om.", 400  # 400 označava neuspešan zahtev
        
        hashed_sifra = hashpw(sifra.encode('utf-8'), gensalt())

        # Kreiraj novog korisnika
        korisnik = Node("Korisnik", ime=ime, prezime=prezime, datum_rodjenja=datum_rodjenja, email=email, sifra=hashed_sifra.decode('utf-8'))
        graph.create(korisnik)

        return "Korisnik uspešno registrovan.", 201  # 201 označava kreiran resurs

    except Exception as e:
        return str(e), 500  # 500 označava internu serversku grešku
    
@korisnik_routes.route('/vrati', methods=['GET'])
def proba():
    return "Dobro",201

@korisnik_routes.route('/obrisiKorisnika',methods=["DELETE"])
def delete():
    try:
        data = request.get_json()
        email=data.get("email")
        graph.run("MATCH (k:Korisnik {email: $email}) DELETE k", email=email)
        return "Korisnik uspešno obrisan.",201
    except Exception as e:
        return str(e), 500  # 500 označava internu serversku grešku
    

@korisnik_routes.route('/aurirajKorisnika',methods=["PUT"])
def update():
    try:
        data = request.get_json()
        email=data.get("email")
        sifra=data.get("sifra")
        nova_sifra=hashpw(sifra.encode('utf-8'), gensalt())

        graph.run("MATCH (k:Korisnik {email: $email}) SET k.sifra = $nova_sifra",
                           email=email, nova_sifra=nova_sifra.decode('utf-8'))
        return "Korisnik uspešno ažuriran."
    except Exception as e:
        return str(e), 500 
    
@korisnik_routes.route('/login')
def login():
    try:
        data = request.get_json()
        email=data.get("email")
        sifra=data.get("sifra")
        result=graph.run("MATCH (k:Korisnik {email: $email}) RETURN k", email=email)
        korisnik = result.evaluate()

        if korisnik:
            heširana_sifra_iz_baze = korisnik.get("sifra")

            # Proveri podudaranje unete šifre sa heširanom šifrom iz baze
            if checkpw(sifra.encode('utf-8'), heširana_sifra_iz_baze.encode('utf-8')):
                return "Uspešno ste se ulogovali."
            else:
                return "Pogrešna šifra.", 401  # 401 označava neautorizovan pristup
        else:
            return "Korisnik sa datim email-om ne postoji.", 404 

    except Exception as e:
        return str(e), 500 