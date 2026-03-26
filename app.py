# app.py - pagrindinė Flask aplokacijos logika
# ŠIAME FAILE APRAŠYTI MARŠRUTAI (routes)

from flask import Flask, render_template, request
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

# Automatinis lenteles sukurimas (paleidimo metu)
# Ši funkcija kvietčiama vieną kartą startuojant aplikacijai
def sukurti_db_lenteles():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        lenteliu_sukurimo_db_uzklausa = """ 
            CREATE TABLE IF NOT EXISTS komentarai (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vardas VARCHAR(100) NOT NULL,
            elpastas VARCHAR(150) NOT NULL,
            zinute TEXT NOT NULL,
            sukurta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
             """

        cursor.execute(lenteliu_sukurimo_db_uzklausa)
        conn.commit()

        cursor.close()
        conn.close()

        print("Lentelė 'Komentarai' sekmingai sukurta")

    except Error as e:
            print("klaida kuriant lentelę", e)

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
    sekme = False
    klaida = None

    if request.method == "POST":
        vardas = request.form.get("vardas")
        elpastas = request.form.get("elpastas")
        zinute = request.form.get("zinute")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            #Įrašome nauja komentarą naudodami parametrizuotą užklausa
            cursor.execute(
                "INSERT INTO komentarai (vardas, elpastas, zinute) VALUES (%s, %s, %s)",
                (vardas, elpastas, zinute)
            )
            conn.commit()

            cursor.close()
            conn.close()

            sekme=True
        except Error as e:
            klaida = f"nepavyko išsaugoti komentaro: {e}"

    return render_template("komentarai.html", klaida=klaida, sekme=sekme )  

# aplikacijos paleidimas
# paleidimo metu kai debbug = True vyksta automatinis aplikacijos perkrovimas pakeitus kodą plius klaidų rodymas
if __name__ == "__main__":
    sukurti_db_lenteles()
    app.run(debug = True)

