from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
from collections import defaultdict
import sqlite3


                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2
  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

#@app.route('/extract-minutes/<date_string>')
#def extract_minutes(date_string):
       # date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        #minutes = date_object.minute
        #return jsonify({'minutes': minutes})


# Route API pour extraire les minutes et compter les commits

@app.route('/commits-data/')

def commits_data():

    # URL de l'API GitHub pour les commits du repository de base

    github_api_url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'

    # 1. Récupération des données depuis l'API GitHub

    try:

        response = urlopen(github_api_url)

        raw_content = response.read()

        json_content = json.loads(raw_content.decode('utf-8'))

    except Exception as e:

        # En cas d'échec de l'API (limite de requêtes, etc.)

        return jsonify({'error': str(e), 'message': 'Impossible de récupérer les données GitHub.'}), 500
 
    # 2. Traitement des données

    # Initialiser un dictionnaire pour stocker le compte des commits par minute

    commits_by_minute = defaultdict(int) 

    # Format de date donné par l'indice N°3 : 2024-02-11T11:57:27Z

    date_format = '%Y-%m-%dT%H:%M:%SZ'

    for commit_entry in json_content:

        # Indice N°2 : La clé de date est [commit][author][date]

        try:

            date_string = commit_entry.get('commit', {}).get('author', {}).get('date')

            if date_string:

                # Convertir la chaîne de date en objet datetime

                date_object = datetime.strptime(date_string, date_format)

                # Extraire la minute (de 0 à 59)

                minute = date_object.minute

                # Compter le commit pour cette minute

                commits_by_minute[minute] += 1

        except Exception:

            # Ignorer les commits sans date ou avec un format invalide

            continue
 
    # 3. Préparer le résultat pour le graphique

    # Convertir le dictionnaire en une liste de paires (Minute, Nombre de commits)

    results = [{'minute': minute, 'count': count} for minute, count in sorted(commits_by_minute.items())]
 
    return jsonify(results=results)
 
# Route pour afficher la page HTML du graphique

@app.route("/commits/")

def commits_page():

    return render_template("commits.html")

 
if __name__ == "__main__":
  app.run(debug=True)
