
import urllib.request
import xmltodict
import datetime  # Bibliothèque pour manipuler les dates et heures
import logging  # Pour le logging
import requests  # Pour interagir avec l'API NewsAPI
import numpy as np
import pickle

# Configuration du logging
logging.basicConfig(level=logging.INFO)

# Partie 1 : Chargement des données

# 1.1 Récupérer les titres des articles depuis NewsAPI
def fetch_newsapi_titles(api_key, query, limit=100):
    try:
        url = f'https://newsapi.org/v2/everything?q={query}&pageSize={limit}&apiKey={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if data['status'] != 'ok':
            logging.error(f"Erreur NewsAPI: {data['message']}")
            return []

        articles = []
        for i, article in enumerate(data['articles']):
            if i % 10 == 0:
                print(f"NewsAPI: {i} / {limit}")
            titre = article['title'].replace("\n", " ").strip()
            auteur = article['author'] if article['author'] else "Auteur Inconnu"
            date = article['publishedAt'] if 'publishedAt' in article else "2023-01-01T00:00:00Z"
            articles.append((titre, "NewsAPI"))
        
        return articles

    except Exception as e:
        logging.error(f"Erreur NewsAPI: {e}")
        return []

# 1.2 Récupérer les titres d'articles depuis Arxiv
def fetch_arxiv_titles(query, max_results=50):
    try:
        url = f'http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}'
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        parsed_data = xmltodict.parse(xml_data)
        articles = []
        for i, entry in enumerate(parsed_data['feed']['entry']):
            if i % 10 == 0:
                print(f"ArXiv: {i} / {max_results}")
            titre = entry['title'].replace("\n", " ").strip()
            auteur = entry['author']['name'] if isinstance(entry['author'], dict) else ", ".join([author['name'] for author in entry['author']])
            auteur = auteur if auteur else "Auteur Inconnu"
            date = entry['published'] if 'published' in entry else "2023-01-01T00:00:00Z"
            articles.append((titre, "ArXiv"))
        return articles
    except Exception as e:
        logging.error(f"Erreur Arxiv: {e}")
        return []

# Récupération des documents depuis NewsAPI et Arxiv
newsapi_key = '3bef90d88eff47159c895ef3ff77f92a'  # Votre clé API NewsAPI
corpus_newsapi = fetch_newsapi_titles(newsapi_key, 'climate', limit=100)  # Récupération des titres NewsAPI
corpus_arxiv = fetch_arxiv_titles('climate', max_results=50)  # Récupération des titres Arxiv

# Combiner les deux corpus
corpus = corpus_newsapi + corpus_arxiv

# Affichage des documents récupérés
print(f"Longueur du corpus : {len(corpus)}")

# Calcul des statistiques
nb_phrases = [len(doc[0].split(".")) for doc in corpus]
nb_mots = [len(doc[0].split(" ")) for doc in corpus]

print("Moyenne du nombre de phrases : " + str(np.mean(nb_phrases)))
print("Moyenne du nombre de mots : " + str(np.mean(nb_mots)))
print("Nombre total de mots dans le corpus : " + str(np.sum(nb_mots)))

# Afficher les informations détaillées pour chaque document
for idx, (titre, source) in enumerate(corpus):
    mots = titre.split()
    nombre_mots = len(mots)
    phrases = titre.split('.')
    nombre_phrases = len([phrase for phrase in phrases if phrase.strip() != ''])
    logging.info(f"Document {idx+1} ({source}):")
    logging.info(f"  - Nombre de mots : {nombre_mots}")
    logging.info(f"  - Nombre de phrases : {nombre_phrases}")
    logging.info(f"  - Titre : {titre[:50] + '...' if len(titre) > 50 else titre}")

# Filtrer les documents contenant plus de 100 caractères
corpus_plus100 = [doc[0] for doc in corpus if len(doc[0]) > 100]

# Créer une chaîne unique contenant tous les documents
chaine_unique = " ".join(corpus_plus100)

# Sauvegarder le corpus dans un fichier pickle
with open("out.pkl", "wb") as f:
    pickle.dump(corpus_plus100, f)

# Charger le corpus depuis le fichier pickle
with open("out.pkl", "rb") as f:
    corpus_plus100 = pickle.load(f)

# Afficher la date et l'heure actuelles
aujourdhui = datetime.datetime.now()
print(aujourdhui)