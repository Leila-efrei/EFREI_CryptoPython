from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Page d'accueil

@app.route('/encrypt/<string:valeur>/<string:key>')
def encryptage(valeur, key):
    """Route pour chiffrer une valeur avec une clé fournie par l'utilisateur"""
    try:
        f = Fernet(key)  # Utilise la clé fournie par l'utilisateur
        valeur_bytes = valeur.encode()  # Conversion str -> bytes
        token = f.encrypt(valeur_bytes)  # Chiffre la valeur
        return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str
    except Exception as e:
        return f"Erreur lors du chiffrement : {str(e)}"  # Gestion des erreurs si la clé est invalide

@app.route('/decrypt/<string:token>/<string:key>')
def decryptage(token, key):
    """Route pour déchiffrer une valeur avec une clé fournie par l'utilisateur"""
    try:
        f = Fernet(key)  # Utilise la clé fournie par l'utilisateur
        decrypted_value = f.decrypt(token.encode())  # Déchiffre le token
        return f"Valeur décryptée : {decrypted_value.decode()}"  # Retourne la valeur décryptée
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"  # Gestion des erreurs si la clé est invalide

@app.route('/key_form', methods=['GET', 'POST'])
def key_form():
    """Formulaire pour entrer la clé et une valeur à chiffrer ou déchiffrer"""
    if request.method == 'POST':
        key = request.form['key']
        valeur = request.form['valeur']
        action = request.form['action']
        
        if action == 'encrypt':
            try:
                f = Fernet(key)
                valeur_bytes = valeur.encode()
                token = f.encrypt(valeur_bytes)
                return f"Valeur encryptée : {token.decode()}"
            except Exception as e:
                return f"Erreur lors du chiffrement : {str(e)}"
        
        elif action == 'decrypt':
            try:
                f = Fernet(key)
                decrypted_value = f.decrypt(valeur.encode())
                return f"Valeur décryptée : {decrypted_value.decode()}"
            except Exception as e:
                return f"Erreur lors du décryptage : {str(e)}"
        
    return '''
        <form method="post">
            Clé (32 bytes) : <input type="text" name="key"><br><br>
            Valeur : <input type="text" name="valeur"><br><br>
            Action : 
            <input type="radio" name="action" value="encrypt"> Chiffrer
            <input type="radio" name="action" value="decrypt"> Déchiffrer<br><br>
            <input type="submit" value="Exécuter">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
