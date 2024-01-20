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
    recept = Node("Recept", naziv=naziv, sastojci=sastojci, opis_pripreme=opis, kategorija=kategorija, ocena=0,broj_ocena=0)
    graph.create(recept)

    # Poveži korisnika sa receptom
    povezi_query = "MATCH (k:Korisnik {email: $email}), (r:Recept {naziv: $naziv}) " \
                   "CREATE (k)-[:POSTAVLJA]->(r)"
    graph.run(povezi_query, email=korisnik_email, naziv=naziv)

    # Poveži recept sa sastojcima
    for sastojak in sastojci:
        sastojak_naziv=sastojak.split(' ' ,1)[1]
        print(sastojak_naziv)
        sastojak_node = graph.run("MERGE (s:Sastojak {naziv: $naziv}) RETURN s", naziv=sastojak_naziv).evaluate()

        if not sastojak_node:
            return f"Sastojak '{sastojak_naziv}' ne postoji."

        povezi_query = "MATCH (r:Recept {naziv: $naziv}), (s:Sastojak {naziv: $sastojak}) " \
                       "CREATE (r)-[:SADRZI]->(s)"
        graph.run(povezi_query, naziv=naziv, sastojak=sastojak_naziv)

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

@recept_routes.route('/vratiRecepte',methods=['GET'])
def vratiRecepte():
    try:
    
        result = graph.run("MATCH (r:Recept) RETURN r").data()
        print(result)
        recepti = [record["r"] for record in result]

        return jsonify({"recepti": recepti}), 200
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

@recept_routes.route('/receptiPoKategoriji', methods=['POST'])
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
    
@recept_routes.route('/receptiPoCeni', methods=["POST"])
def receptiPoCeni():
    try:
        data=request.get_json()
        cenaOd=data.get("cenaOd")
        cenaDo=data.get("cenaDo")
        if cenaOd is None:
            cenaOd=0
        print(cenaOd,cenaDo)
        result = graph.run("MATCH (r:Recept) RETURN r")
        recepti = [record["r"] for record in result]
        ukupna_cena=0
        query = """
      MATCH (r:Recept)
        OPTIONAL MATCH (r)-[:SADRZI]->(s:Sastojak)
        RETURN DISTINCT r, COLLECT(s) AS sastojci

        """

        result = graph.run(query)
        recepti_sastojci = []

        for record in result:
            recept = record.get("r")
            sastojci = record.get("sastojci")

            if recept and sastojci:
                print(f"Recept: {recept}")
                print(f"Sastojci: {sastojci}")

                # Dodajte dodatne provere ili ispisivanje podataka po potrebi

                recepti_sastojci.append((recept, sastojci))
            else:
                print(f"I preskačem zapis zbog nedostajućih podataka. Zapis: {record}")

        print(recepti_sastojci)
        odgovarajuci_recepti=[]
        for recept, sastojak in recepti_sastojci:
            for sastojak_unos in recept["sastojci"]:
                kolicina, sastojak_naziv = map(str.strip, sastojak_unos.split(' ', 1))
                print(sastojak_naziv)
                print(kolicina)
                sastojak_node = graph.run("MERGE (s:Sastojak {naziv: $naziv}) RETURN s", naziv=sastojak_naziv).evaluate()

                if sastojak_node:
                    cena_sastojka = sastojak_node.get("cena", 0)
                    print(cena_sastojka)
                    kol=float(kolicina[:-2])
                    cena=float(cena_sastojka[:-3])
                    trenutna_cena = (kol  * cena)/100  # Ukloni 'gr' i pretvori u float
                    print(trenutna_cena)

                ukupna_cena=ukupna_cena+trenutna_cena
            print(ukupna_cena)
            if float(cenaOd) <= float(ukupna_cena) <= float(cenaDo):
                odgovarajuci_recepti.append(recept)

        return jsonify({"recepti": odgovarajuci_recepti})

        

    except Exception as e:
        return str(e), 500

@recept_routes.route('/dodajOcenuReceptu', methods=["POST"])
def dodajOcenuReceptu():
    try:
        data = request.get_json()
        nova_ocena = data.get("ocena")
        naziv_recepta = data.get("naziv_recepta")
        nova_ocena=(float)(nova_ocena)
        # Proveri da li postoji recept sa datim nazivom
        existing_recept = graph.run("MATCH (r:Recept {naziv: $naziv_recepta}) RETURN r", naziv_recepta=naziv_recepta)
        existing_recept = existing_recept.evaluate()

        if not existing_recept:
            return "Recept sa datim nazivom ne postoji."

        # Ako postoji recept, ažuriraj ocenu
        trenutna_ocena = existing_recept.get("ocena")
        broj_ocena = existing_recept.get("broj_ocena") + 1
        if(broj_ocena==0):
            nova_ocena=nova_ocena
        else:
            nova_ocena = (trenutna_ocena + nova_ocena) / 2
        

        # Ažuriraj vrednost ocene i broj ocena u čvoru Recept
        query = """
        MATCH (r:Recept {naziv: $naziv_recepta})
        SET r.ocena = $nova_ocena
        SET r.broj_ocena = $broj_ocena
        RETURN r
        """
        graph.run(query, naziv_recepta=naziv_recepta, nova_ocena=nova_ocena, broj_ocena=broj_ocena)

        return f"Ocena recepta '{naziv_recepta}' uspešno ažurirana na {nova_ocena}."

    except Exception as e:
        return str(e), 500

@recept_routes.route('/nutritivnaVrednostRecepta',methods=['POST'])
def nutritivnaVrednostRecepta():
    try:
        data=request.get_json()
        recept=data.get("naziv")

        result=graph.run("""MATCH (r:Recept {naziv: "Proba4"})-[:SADRZI]->(s:Sastojak)
                            WITH r.sastojci AS naziv_sastojka, s
                            RETURN 
                              naziv_sastojka AS naziv_sastojka,
                              COLLECT(DISTINCT s.kalorijska_vrednost) AS kalorijska_vrednost,
                              COLLECT(DISTINCT s.proteini) AS proteini,
                              COLLECT(DISTINCT s.masti) AS masti,
                              COLLECT(DISTINCT s.ugljeni_hidrati) AS ugljeni_hidrati""").data()
        
        sastojci = result[0]['naziv_sastojka']
        kalorijska_vrednost = result[0]['kalorijska_vrednost']
        proteini = result[0]['proteini']
        masti = result[0]['masti']
        ugljeni_hidrati = result[0]['ugljeni_hidrati']
        print(sastojci,kalorijska_vrednost,proteini,masti,ugljeni_hidrati)
        sumKCAL=0
        sumUH=0
        sumM=0
        sumP=0

        for i in range(len(sastojci)):
            kolicina_string, sastojak_naziv = map(str.strip, sastojci[i].split(' ', 1))
            kolicina = float(''.join(filter(str.isdigit, kolicina_string)))
            print(sastojak_naziv)
            print(kolicina)
            kalorije=float(''.join(filter(str.isdigit, kalorijska_vrednost[i])))
            print(kalorije)
            sumKCAL+=kolicina*kalorije/100
            uh=float(ugljeni_hidrati[i])
            m=float(masti[i])
            p=float(proteini[i])
            sumUH+=kolicina*uh/100
            sumM+=kolicina*m/100
            sumP+=kolicina*p/100
            print("suma", sumKCAL)

        # Nastavite sa ostatkom koda...

        return jsonify({
            "SumKCAL": sumKCAL,
            "SumUH": sumUH,
            "SumM": sumM,
            "SumP": sumP
        }), 200
    
    except Exception as e:
        return str(e), 500
    



@recept_routes.route('/trenutnaVrdnostRecepta',methods=['GET'])
def trenutnaVrdnostRecepta():
     try:
        data=request.get_json()
        recept=data.get("naziv")



     except Exception as e:
        return str(e), 500
    