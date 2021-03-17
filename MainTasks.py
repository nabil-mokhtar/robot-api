from flask import Flask, request, jsonify
import requests,json
from flask_restful import Api ,Resource

DjangoProject="http://127.0.0.1:8000/"


app = Flask(__name__)
api = Api(app)


