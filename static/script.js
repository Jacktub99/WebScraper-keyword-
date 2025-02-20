// Funzione asincrona per effettuare la ricerca dei risultati SERP tramite una keyword inserita dall'utente.
async function searchSERP() {
    // Prende il valore della keyword dall'input dell'utente.
    const keyword = document.getElementById("keywordInput").value;

    // Se la keyword non è stata inserita, mostra un avviso e termina l'esecuzione della funzione.
    if (!keyword) {
        alert("Inserisci una keyword!");
        return;
    }

    // Esegue una richiesta POST al server per inviare la keyword al backend e ottenere i risultati della ricerca.
    const response = await fetch("/search", {
        method: "POST", // Metodo della richiesta
        headers: { "Content-Type": "application/json" }, // Specifica che il corpo della richiesta è in formato JSON
        body: JSON.stringify({ keyword }) // Converte la keyword in una stringa JSON da inviare al server
    });

    // Converte la risposta ricevuta dal server in formato JSON.
    const results = await response.json();

    // Se nella risposta c'è un errore, mostra l'errore all'utente e interrompe l'esecuzione.
    if (results.error) {
        alert(results.error);
        return;
    }

    // Se i risultati sono stati trovati, chiama la funzione displayResults per mostrarli.
    displayResults(results);
}

// Funzione per visualizzare i risultati della ricerca nella tabella HTML.
function displayResults(results) {
    // Seleziona il corpo della tabella dove verranno aggiunti i risultati.
    const tableBody = document.querySelector("#resultsTable tbody");

    // Svuota il contenuto della tabella prima di aggiungere i nuovi risultati.
    tableBody.innerHTML = "";

    // Per ogni risultato della ricerca, crea una nuova riga nella tabella.
    results.forEach((res, index) => {
        // Crea una nuova riga (tr) per ogni risultato.
        const tr = document.createElement("tr");
        
        // Imposta il contenuto HTML della riga con i dati del risultato (indice, link, titolo e pulsante per l'analisi).
        tr.innerHTML = `
            <td>${index + 1}</td> <!-- Mostra il numero di posizione del risultato -->
            <td><a href="${res.link}" target="_blank">${res.link}</a></td> <!-- Link al risultato -->
            <td>${res.title}</td> <!-- Titolo del risultato -->
            <td><button onclick="analyzePage('${res.link}')">Analizza</button></td> <!-- Bottone per analizzare la pagina -->
        `;

        // Aggiunge la riga appena creata alla tabella.
        tableBody.appendChild(tr);
    });
}

// Funzione asincrona per analizzare una pagina specifica quando l'utente clicca sul pulsante "Analizza".
async function analyzePage(url) {
    // Prende la keyword inserita dall'utente per eseguire l'analisi.
    const keyword = document.getElementById("keywordInput").value;

    // Invia una richiesta POST al server per analizzare la pagina specificata, inviando l'URL e la keyword.
    const response = await fetch("/analyze", {
        method: "POST", // Metodo della richiesta
        headers: { "Content-Type": "application/json" }, // Specifica che il corpo della richiesta è in formato JSON
        body: JSON.stringify({ url, keyword }) // Converte l'URL e la keyword in una stringa JSON
    });

    // Converte la risposta ricevuta dal server in formato JSON.
    const analysis = await response.json();

    // Se c'è un errore nella risposta, mostra l'errore all'utente e termina l'esecuzione.
    if (analysis.error) {
        alert(analysis.error);
        return;
    }

    // Se l'analisi è andata a buon fine, chiama la funzione displayAnalysis per mostrare i risultati dell'analisi.
    displayAnalysis(analysis);
}

// Funzione per visualizzare i risultati dell'analisi della pagina.
function displayAnalysis(analysis) {
    // Seleziona l'elemento div dove verranno visualizzati i risultati dell'analisi.
    const analysisDiv = document.getElementById("analysisResults");

    // Imposta il contenuto HTML del div con i dati dell'analisi (URL, titolo, meta description, densità della keyword, numero di parole).
    analysisDiv.innerHTML = `
        <h3>URL: ${analysis.url}</h3> <!-- Mostra l'URL della pagina analizzata -->
        <p><strong>Title:</strong> ${analysis.title}</p> <!-- Mostra il titolo della pagina -->
        <p><strong>Meta Description:</strong> ${analysis.meta_description}</p> <!-- Mostra la meta description della pagina -->
        <p><strong>Keyword Density:</strong> ${analysis.keyword_density.toFixed(2)}%</p> <!-- Mostra la densità della keyword -->
        <p><strong>Word Count:</strong> ${analysis.word_count}</p> <!-- Mostra il numero totale di parole nella pagina -->
    `;
}
