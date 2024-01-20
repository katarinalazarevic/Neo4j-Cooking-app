from flask import request,jsonify, Blueprint
from py2neo import Graph, Node
from bcrypt import checkpw, hashpw, gensalt
from Models.sastojak import Sastojak
from database import graph
sastojak_routes = Blueprint("sastojak_routes", __name__)

@sastojak_routes.route('/dodajSastojak', methods=["POST"])
def dodajSastojak():
    try:
        data = request.get_json()
        naziv = data.get("naziv")
        kalorijska_vrednost = data.get("kalorijska_vrednost")
        proteini = data.get("proteini")
        masti = data.get("masti")
        ugljeni_hidrati = data.get("ugljeni_hidrati")
        cena = data.get("cena")
        
        oldsastojak = graph.run("MATCH (s:Sastojak {naziv: $naziv}) RETURN s", naziv=naziv)
        
        if oldsastojak is not None and oldsastojak.evaluate():
            return "Sastojak sa datim nazivom već postoji."

        # Kreiraj novi sastojak
        sastojak = Node("Sastojak", naziv=naziv, kalorijska_vrednost=kalorijska_vrednost, proteini=proteini, masti=masti, ugljeni_hidrati=ugljeni_hidrati, cena=cena)
        graph.create(sastojak)
        
        return "Sastojak uspešno dodat."
    except Exception as e:
        return str(e), 500  

    
@sastojak_routes.route('/obrisiSastojak', methods=["DELETE"])
def obrisiSastojak():
    try:
        data = request.get_json()
        naziv = data.get("naziv")

       
        existing_sastojak = graph.run("MATCH (s:Sastojak {naziv: $naziv}) RETURN s", naziv=naziv).evaluate()

        if not existing_sastojak:
            return "Sastojak sa datim nazivom ne postoji.", 404

        graph.run("MATCH (s:Sastojak {naziv: $naziv}) DELETE s", naziv=naziv)

        return "Sastojak uspešno obrisan.", 200
    except Exception as e:
        return str(e), 500


@sastojak_routes.route('/azurirajSastojak', methods=["POST"])
def azurirajSastojak():
    try:
        data = request.get_json()
        naziv = data.get("naziv")
        nova_cena = data.get("nova_cena")

        # Proveri da li sastojak sa datim nazivom postoji
        existing_sastojak = graph.run("MATCH (s:Sastojak {naziv: $naziv}) RETURN s", naziv=naziv).evaluate()

        if not existing_sastojak:
            return f"Sastojak sa nazivom '{naziv}' ne postoji.", 404

        # Ažuriraj cenu sastojka
        graph.run("MATCH (s:Sastojak {naziv: $naziv}) SET s.cena = $nova_cena", naziv=naziv, nova_cena=nova_cena)

        print("DEBUG: Cena sastojka uspešno ažurirana.")

        return "Cena sastojka uspešno ažurirana.", 200
    except Exception as e:
        print(f"ERROR: Greška prilikom ažuriranja cene sastojka - {str(e)}")
        return str(e), 500


@sastojak_routes.route('/vratiSastojke', methods=["GET"])
def vratiSastojke():
    try:
        result = graph.run("MATCH (s:Sastojak) RETURN s")
        sastojci = [record["s"] for record in result]

        return jsonify({"sastojci": sastojci}), 200
    except Exception as e:
        print(f"ERROR: Greška prilikom vraćanja sastojaka - {str(e)}")
        return str(e), 500

from flask import jsonify

@sastojak_routes.route('/vratiSastojak', methods=["POST"])
def vratiSastojak():
    try:
      
        data = request.get_json()
        naziv = data.get("naziv")
        sastojak = graph.run("MATCH (s:Sastojak {naziv: $naziv}) RETURN s", naziv=naziv).evaluate()

        if not sastojak:
            return f"Sastojak sa nazivom '{naziv}' ne postoji.", 404
        return sastojak, 200
        
    except Exception as e:
        return str(e), 500
       
      


@sastojak_routes.route('/nutritivneVrednostiSastojka', methods=['POST'])
def nutritivneVrednostiSastojka():
    try:
        data = request.get_json()
        naziv = data.get("naziv")
        
        query = """
            MATCH (s:Sastojak {naziv: $naziv})
            RETURN s
        """

        result = graph.run(query, naziv=naziv)
        sastojak_info = result.evaluate()

        if not sastojak_info:
            return {"error": "Sastojak nije pronadjen"}, 404

        naziv = sastojak_info["naziv"]
        kalorijska_vrednost = sastojak_info["kalorijska_vrednost"]
        proteini = sastojak_info["proteini"]
        masti = sastojak_info["masti"]
        ugljeni_hidrati = sastojak_info["ugljeni_hidrati"]

        return jsonify({
            "Naziv": naziv,
            "Kalorijska vrednost": kalorijska_vrednost,
            "Proteini": proteini,
            "Masti": masti,
            "Ugljeni hidrati": ugljeni_hidrati
        }), 200

       

    except Exception as e:
        return str(e), 500

