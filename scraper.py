# Importazione delle librerie necessarie
import requests  # Per effettuare richieste HTTP
from bs4 import BeautifulSoup  # Per fare il parsing del codice HTML e estrarre dati dalle pagine web
import pandas as pd  # (Non utilizzato nel codice, ma potenzialmente utile per la gestione dei dati)
import time  # Per introdurre ritardi tra le richieste (utile per evitare di essere bloccati dai server)
import random  # Per generare numeri casuali, usato per variare il tempo di attesa tra le richieste

# Definizione della classe SerpScraper
class SerpScraper:
    def __init__(self):
        # Intestazioni per la richiesta HTTP, per simulare un browser e evitare di essere bloccati da un sistema di protezione
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0 Safari/537.36"
        }

    # Metodo per ottenere i risultati della SERP (Search Engine Results Page) per una keyword
    def get_serp_results(self, keyword, num_results=20):
        # URL di base per la ricerca su Bing
        base_url = "https://www.bing.com/search"
        
        # Parametri per la ricerca, inclusa la keyword fornita
        params = {"q": keyword}

        # Effettua la richiesta GET per ottenere la pagina dei risultati di ricerca
        response = requests.get(base_url, headers=self.headers, params=params)

        # Introduce un ritardo casuale tra 2 e 5 secondi per evitare il blocco da parte del server
        time.sleep(random.uniform(2, 5))
        
        # Se la risposta non ha successo (status code diverso da 200), ritorna una lista vuota
        if response.status_code != 200:
            return []

        # Usa BeautifulSoup per fare il parsing del contenuto HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Lista per contenere i risultati della ricerca
        search_results = []

        # Estrazione dei titoli e dei link dei risultati dalla SERP
        for item in soup.select("h2 a"):
            title = item.get_text()  # Estrae il testo (titolo)
            link = item.get("href")  # Estrae l'attributo href (link)
            
            # Se sia il titolo che il link sono validi, aggiungili alla lista dei risultati
            if title and link:
                search_results.append({"title": title, "link": link})

        # Restituisce i risultati della ricerca (un elenco di dizionari contenenti titolo e link)
        return search_results

    # Metodo per analizzare una pagina web e calcolare alcune metriche SEO
    def analyze_page(self, url, keyword):
        try:
            # Effettua la richiesta GET per ottenere il contenuto della pagina
            response = requests.get(url, headers=self.headers)

            # Se la risposta non ha successo (status code diverso da 200), ritorna None
            if response.status_code != 200:
                return None

            # Usa BeautifulSoup per fare il parsing del contenuto HTML della pagina
            soup = BeautifulSoup(response.text, "html.parser")

            # Estrae il titolo della pagina, se presente
            title = soup.title.string if soup.title else "No title"

            # Estrae la meta description dalla pagina, se presente
            meta_description = soup.find("meta", attrs={"name": "description"})
            meta_description = meta_description.get("content", "") if meta_description else ""

            # Conta il numero totale di parole nel testo della pagina
            word_count = len(soup.get_text(separator=" ").split())

            # Conta quante volte la keyword appare nel testo della pagina
            keyword_count = soup.get_text(separator=" ").lower().count(keyword.lower())

            # Calcola la densità della keyword (percentuale della keyword nel totale delle parole)
            keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0

            # Restituisce un dizionario con i risultati dell'analisi
            return {
                "url": url,  # URL della pagina analizzata
                "title": title,  # Titolo della pagina
                "meta_description": meta_description,  # Meta description della pagina
                "keyword_density": keyword_density,  # Densità della keyword nella pagina
                "word_count": word_count  # Numero di parole nella pagina
            }

        # In caso di errore, restituisce None
        except:
            return None
