from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import json
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

# Clé de chiffrement
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Affiche la page de base

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    """Route pour chiffrer une valeur"""
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Chiffre la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:token>')
def decryptage(token):
    """Route pour déchiffrer une valeur"""
    try:
        # Décryptage du token
        decrypted_value = f.decrypt(token.encode())  # Déchiffre le token
        return f"Valeur décryptée : {decrypted_value.decode()}"  # Retourne la valeur décryptée
    except Exception as e:
        # Si le décryptage échoue (par exemple si le token est invalide)
        return f"Erreur lors du décryptage : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
