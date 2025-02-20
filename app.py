# Importazione delle librerie necessarie
from flask import Flask, render_template, request, jsonify  # Flask per la creazione dell'app, render_template per il rendering dei template HTML, request per gestire le richieste HTTP, jsonify per restituire risposte JSON
from scraper import SerpScraper  # Importazione della classe SerpScraper, che probabilmente contiene le funzioni di scraping per ottenere i risultati della ricerca
from flask_cors import CORS  # Importazione di CORS per gestire le richieste Cross-Origin Resource Sharing (per consentire la comunicazione tra frontend e backend su domini diversi)

# Creazione dell'app Flask
app = Flask(__name__)

# Abilitazione di CORS per l'app, per permettere al frontend di fare richieste HTTP al server backend
CORS(app)

# Creazione dell'istanza dello scraper, che verrà utilizzata per ottenere i risultati della SERP e per analizzare le pagine
scraper = SerpScraper()

# Rotta per la home page, che restituisce il template HTML principale
@app.route('/')
def home():
    # Renderizza il template HTML della home page
    return render_template('index.html')

# Rotta per eseguire una ricerca sulla SERP, si aspetta una richiesta POST con una keyword
@app.route('/search', methods=['POST'])
def search():
    # Estrazione dei dati dalla richiesta JSON
    data = request.json
    keyword = data.get("keyword")  # Estrazione della keyword dalla richiesta

    # Verifica che la keyword sia presente
    if not keyword:
        # Se la keyword non è presente, restituisce un errore con codice 400 (Bad Request)
        return jsonify({"error": "Inserisci una keyword valida!"}), 400

    # Esegui la ricerca della SERP con la keyword fornita, limitando i risultati a 10
    results = scraper.get_serp_results(keyword, num_results=10)

    # Verifica se sono stati trovati dei risultati
    if not results:
        # Se non sono stati trovati risultati, restituisce un errore con codice 404 (Not Found)
        return jsonify({"error": "Nessun risultato trovato!"}), 404

    # Restituisce i risultati della ricerca come risposta JSON
    return jsonify(results)

# Rotta per analizzare una pagina specifica, si aspetta una richiesta POST con l'URL e la keyword
@app.route('/analyze', methods=['POST'])
def analyze():
    # Estrazione dei dati dalla richiesta JSON
    data = request.json
    url = data.get("url")  # Estrazione dell'URL della pagina da analizzare
    keyword = data.get("keyword")  # Estrazione della keyword per l'analisi

    # Verifica che siano presenti sia l'URL che la keyword
    if not url or not keyword:
        # Se manca l'URL o la keyword, restituisce un errore con codice 400 (Bad Request)
        return jsonify({"error": "URL e keyword sono richiesti!"}), 400

    # Esegui l'analisi della pagina utilizzando lo scraper
    analysis = scraper.analyze_page(url, keyword)

    # Verifica se l'analisi è stata eseguita correttamente
    if not analysis:
        # Se l'analisi non è riuscita, restituisce un errore con codice 500 (Internal Server Error)
        return jsonify({"error": "Analisi non riuscita!"}), 500

    # Restituisce i risultati dell'analisi come risposta JSON
    return jsonify(analysis)

# Avvio dell'app in modalità debug
if __name__ == '__main__':
    app.run(debug=True)
