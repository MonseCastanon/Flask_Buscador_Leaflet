from flask import Flask, render_template, request
import requests

# Importando la librería de Flask
app = Flask(__name__)

# Se crea un objeto app con su propiedad __name__
@app.route('/')
def index():
    return render_template('index.html')

# Se define la respuesta por medio de un método para la ruta especificada
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        lugar = request.form['lugar']

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": lugar,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "Flask-Educational-App"
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            nombre = data[0]['display_name']

            return render_template(
                'map.html',
                lat=lat,
                lon=lon,
                nombre=nombre
            )

    return render_template('map.html', error="")

if __name__=='__main__':
    app.run(debug=True)