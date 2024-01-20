from ast import Constant
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
    
        existing_user = existing_user.evaluate()

        if existing_user:
            return "Korisnik već postoji sa ovim email-om.", 400  
        
        hashed_sifra = hashpw(sifra.encode('utf-8'), gensalt())

        # Kreiraj novog korisnika
        korisnik = Node("Korisnik", ime=ime, prezime=prezime, datum_rodjenja=datum_rodjenja, email=email, sifra=hashed_sifra.decode('utf-8'))
        graph.create(korisnik)

        return jsonify({'message': 'SUCCESS'}), 201
       

    except Exception as e:
        return str(e), 500  # 500 označava internu serversku grešku
    
@korisnik_routes.route('/vratiKorisnika', methods=['GET'])
def vratiKorisnika():
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
    
@korisnik_routes.route('/login', methods=["POST"])
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
                 response ={
                    "korisnik": korisnik,
                    "message": "SUCCESS"
                }
                 #return jsonify({'message': 'SUCCESS', 'ime': korisnik}), 200
                 return response, 200
            else:
                return "Pogrešna šifra.", 401  # 401 označava neautorizovan pristup
        else:
            return "Korisnik sa datim email-om ne postoji.", 404 

    except Exception as e:
        return str(e), 500 
@korisnik_routes.route('/zapratiKorisnika', methods=['POST'])
def zapratiKorisnika():
    try:
        data = request.get_json()
        korisnik1email = data.get("korisnik1")
        korisnik2email = data.get("korisnik2")

        # Provera da li korisnici postoje
        korisnik1 = graph.run("MATCH (korisnik1:Korisnik {email: $email}) RETURN korisnik1", email=korisnik1email).data()
        korisnik2 = graph.run("MATCH (korisnik2:Korisnik {email: $email}) RETURN korisnik2", email=korisnik2email).data()

        if not korisnik1:
            return "Korisnik sa datim email-om ne postoji.", 404
        elif not korisnik2:
            return "Korisnik sa datim email-om ne postoji.", 404

        #  upit za praćenje korisnika
        pratilac_query = """
        MATCH (korisnik1:Korisnik {email: $email1}), (korisnik2:Korisnik {email: $email2})
        CREATE (korisnik1)-[:PRAĆENJE]->(korisnik2)
        """
        graph.run(pratilac_query, email1=korisnik1email, email2=korisnik2email)

        return "Uspešno praćenje korisnika.", 200

    except Exception as e:
        return str(e), 500

@korisnik_routes.route('/otpratiKorisnika', methods=['POST'])
def otpratiKorisnika():
    try:
        data = request.get_json()
        korisnik1email = data.get("korisnik1")
        korisnik2email = data.get("korisnik2")

        # Provera da li korisnici postoje
        korisnik1 = graph.run("MATCH (korisnik1:Korisnik {email: $email}) RETURN korisnik1", email=korisnik1email).data()
        korisnik2 = graph.run("MATCH (korisnik2:Korisnik {email: $email}) RETURN korisnik2", email=korisnik2email).data()

        if not korisnik1:
            return "Korisnik sa datim email-om ne postoji.", 404
        elif not korisnik2:
            return "Korisnik sa datim email-om ne postoji.", 404

        #upit za otpraćivanje korisnika
        otprati_query = """
        MATCH (korisnik1:Korisnik {email: $email1})-[pracenje:PRAĆENJE]->(korisnik2:Korisnik {email: $email2})
        DELETE pracenje
        """
        graph.run(otprati_query, email1=korisnik1email, email2=korisnik2email)

        return "Uspešno otpraćivanje korisnika.", 200

    except Exception as e:
        return str(e), 500

@korisnik_routes.route('/receptiKorisnikaKojePratim', methods=['POST'])
def receptiKorisnikaKojePratim():
    try:
        data = request.get_json()
        korisnik_email = data.get("korisnik")

        korisnik = graph.run("MATCH (k:Korisnik {email: $email}) RETURN k", email=korisnik_email).data()

        if not korisnik:
            return "Korisnik sa datim email-om ne postoji.", 404

        recepti_query = """
        MATCH (korisnik:Korisnik {email: $email})-[:PRAĆENJE]->(praceni:Korisnik)-[:POSTAVLJA]->(recept:Recept)
        RETURN DISTINCT recept
        """
        recepti_pracenih_korisnika = graph.run(recepti_query, email=korisnik_email).data()

        return jsonify({"recepti": recepti_pracenih_korisnika}), 200

    except Exception as e:
        return str(e), 500



