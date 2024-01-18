from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from neo4j import GraphDatabase
from py2neo import Graph
from flask_cors import CORS
from Routes.korisnikRoutes import korisnik_routes
from Routes.receptRoutes import recept_routes
from Routes.sastojakRoutes import sastojak_routes
from Routes.komentarRoutes import komentar_routes

app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

app.register_blueprint(korisnik_routes)
app.register_blueprint(recept_routes)
app.register_blueprint(sastojak_routes)
app.register_blueprint(komentar_routes)


# Postavi Neo4j konekciju
uri = "bolt://localhost:7687"
username = "neo4j"
password = "kacabaze"
#graph = Graph("bolt://localhost:7687", auth=("neo4j", "kacabaze"))



if __name__ == "__main__":
    app.run(debug=True)
