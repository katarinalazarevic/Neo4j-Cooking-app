from flask import request,jsonify, Blueprint
from py2neo import Graph, Node
from bcrypt import checkpw, hashpw, gensalt
from database import graph
sastojak_routes = Blueprint("sastojak_routes", __name__)

@sastojak_routes.route('/dodajSastojak',methods=["POST"])
def dodajSastojak():
    try:

        data=request.get_json()
        naziv=data.get("naziv")
        kalorijska_vrednost=data.get("kalorijska_vrednost")
        proteini=data.get("proteini")
        masti=data.get("masti")
        ugljeni_hidrati=data.get("ugljeni_hidrati")
        cena=data.get("cena")
        oldsastojak = graph.run("MATCH (s:Sastojak {naziv: $naziv}) RETURN s", naziv=naziv)
        oldsastojak=oldsastojak.evaluate()

        if oldsastojak:
            return "Sastojak sa datim nazivom već postoji."
        # Kreiraj novi sastojak
        sastojak = Node("Sastojak", naziv=naziv,kalorijska_vrednost=kalorijska_vrednost,proteini=proteini,masti=masti,ugljeni_hidrati=ugljeni_hidrati,cena=cena)
        graph.create(sastojak)
        return "Sastojak uspešno dodat."
    except Exception as e:
        return str(e), 500  # 500 označava internu serversku grešku
    
@sastojak_routes.route('/obrisiSastojak',methods=["DELETE"])
def obrisiSastojak():
    try:
        data=request.json()
        naziv=data.get("naziv")
        graph.run("MATCH (s:Sastojak {naziv: $naziv}) DELETE s", naziv=naziv)
        return "Sastojak uspešno obrisan.",201
    except Exception as e:
        return str(e), 500

@sastojak_routes.route('/azurirajSastojak',methods=["POST"])
def azurirajSastojak():
    try:
        data = request.json()
        naziv = data.get("naziv")
        nova_cena = data.get("nova_cena")
    
        # Proveri da li sastojak sa datim nazivom postoji
        sastojak = graph.run("MATCH (s:Sastojak {naziv: $naziv}) RETURN s", naziv=naziv)
        sastojak=sastojak.evaluate()

        if not sastojak:
            return f"Sastojak sa nazivom '{naziv}' ne postoji.", 404

        # Ažuriraj cenu sastojka
        graph.run("MATCH (s:Sastojak {naziv: $naziv}) SET s.cena = $nova_cena", naziv=naziv, nova_cena=nova_cena)

        print("DEBUG: Cena sastojka uspešno ažurirana.")

        return "Cena sastojka uspešno ažurirana.", 200
    except Exception as e:
        print(f"ERROR: Greška prilikom ažuriranja cene sastojka - {str(e)}")
        return str(e), 500


def vratiSastojke():
    try:
        result = graph.run("MATCH (s:Sastojak) RETURN s")
        sastojci = [record["s"] for record in result]

        return jsonify({"sastojci": sastojci}), 200
    except Exception as e:
        print(f"ERROR: Greška prilikom vraćanja sastojaka - {str(e)}")
        return str(e), 500
