# app.py - pagrindinė Flask aplokacijos logika
# ŠIAME FAILE APRAŠYTI MARŠRUTAI (routes)

from flask import Flask, render_template

# sukuriame flask aplikacijos objektą
app = Flask(__name__)

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
def kontaktai():
    return render_template("apie.html")    

# aplikacijos paleidimas
# paleidimo metu kai debbug = True vyksta automatinis aplikacijos perkrovimas pakeitus kodą plius klaidų rodymas
if __name__ == "__main__":
    app.run(debug = True)

