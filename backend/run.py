from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from neo4j import GraphDatabase
from py2neo import Graph
from Routes.korisnikRoutes import korisnik_routes
from Routes.receptRoutes import recept_routes
from Routes.sastojakRoutes import sastojak_routes

app = Flask(__name__)
api = Api(app)

app.register_blueprint(korisnik_routes)
app.register_blueprint(recept_routes)
app.register_blueprint(sastojak_routes)


# Postavi Neo4j konekciju
uri = "bolt://localhost:7687"
username = "neo4j"
password = "kacabaze"
#graph = Graph("bolt://localhost:7687", auth=("neo4j", "kacabaze"))



if __name__ == "__main__":
    app.run(debug=True)
