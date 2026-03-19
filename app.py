# app.py - pagrindinė Flask aplokacijos logika
# ŠIAME FAILE APRAŠYTI MARŠRUTAI (routes)

from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv # .env failo nuskaitimai

# sukuriame flask aplikacijos objektą
app = Flask(__name__)

# Duomenų bazes prijungimas
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT",3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# maršrutas DB prisijungimas testas
@app.route("/db-testas")
def db_testas():
    try:
        conn = get_db_connection()
        if conn.is_connected():
            return "prisijungimas prie sql pavyko!"
        else:
            return "prisijungimas nepavyko :("
    except Error as e:
        return f"klaida jungentis: {e}"

# užkrauname aplinkos kintamuosius iš .env failo
load_dotenv()

# Maršrutas: pagrindinis puslapis
# URL:/
# Metodas: GET
# atvaizduoja index.html šabloną
@app.route("/") # Dekoratorius
def index():
    return render_template("index.html")

# Maršrutas: kontaktų puslapis (forma)
# Metodai: GET ir POST
@app.route("/apie")
def apie():
    return render_template("apie.html")    

@app.route("/kontaktai")
def kontaktai():
    return render_template("kontaktai.html")  

@app.route("/komentarai", methods=["GET", "POST"])
def komentarai():
    return render_template("komentarai.html")  

# aplikacijos paleidimas
# paleidimo metu kai debbug = True vyksta automatinis aplikacijos perkrovimas pakeitus kodą plius klaidų rodymas
if __name__ == "__main__":
    app.run(debug = True)

