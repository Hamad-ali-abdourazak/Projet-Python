import urllib.request
import xmltodict
import datetime  # Bibliothèque pour manipuler les dates et heures
from Classes import Document  # Importation de la classe Document
from Classes import Author  # Importation de la classe Author
from Corpus import Corpus  # Importation de la classe Corpus
import pickle  # Utilisé pour la sérialisation des objets Python
from prettytable import PrettyTable  # Pour un affichage tabulaire des résultats
import requests  # Pour interagir avec l'API NewsAPI
import logging  # Pour le logging

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
            articles.append((titre, auteur, date))
        
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
            articles.append((titre, auteur, date))
        return articles
    except Exception as e:
        logging.error(f"Erreur Arxiv: {e}")
        return []

# Récupération des documents depuis NewsAPI et Arxiv
newsapi_key = '3bef90d88eff47159c895ef3ff77f92a'  # Votre clé API NewsAPI
corpus_newsapi = fetch_newsapi_titles(newsapi_key, 'climate', limit=100)  # Récupération des titres NewsAPI
corpus_arxiv = fetch_arxiv_titles('climate', max_results=50)  # Récupération des titres Arxiv

# Combiner les deux corpus
docs = corpus_newsapi + corpus_arxiv

# Affichage des documents récupérés
print(f"# docs avec doublons : {len(docs)}")
docs = list(set(docs))  # Supprimer les doublons en convertissant en un set puis en liste
print(f"# docs sans doublons : {len(docs)}")

# Suppression des documents trop courts
for i, (titre, auteur, date) in enumerate(docs):
    print(f"Document {i}\t# caractères : {len(titre)}\t# mots : {len(titre.split(' '))}\t# phrases : {len(titre.split('.'))}")
    if len(titre) < 100:  # Suppression des documents dont la longueur est inférieure à 100 caractères
        docs.remove((titre, auteur, date))

# Création d'une chaîne de texte avec tous les documents restants
longueChaineDeCaracteres = " ".join([titre for titre, auteur, date in docs])

# Construction des objets Document à partir des données NewsAPI et ArXiv
collection = []
for titre, auteur, date in docs:
    # Convertir la date au format '%Y/%m/%d'
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    date_str = date_obj.strftime('%Y/%m/%d')
    document = Document(titre=titre, auteur=auteur, date=date_str, url="", texte=titre)
    collection.append(document)

# Création d'un index des documents
id2doc = {i: doc.titre for i, doc in enumerate(collection)}

# Gestion des auteurs
authors = {}
aut2id = {}
num_auteurs_vus = 0

# Création d'une liste des auteurs et association avec les documents
for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc)

# Création du Corpus
corpus = Corpus("Mon corpus")

# Ajout des documents au corpus
for doc in collection:
    corpus.add(doc)

# FONCTIONS D'AFFICHAGE RAFFINÉ 

# Fonction pour afficher un résumé statistique du corpus
def afficher_statistiques(corpus):
    print("=== Résumé du Corpus ===")
    print(f"Nom du Corpus : {corpus.nom}")
    print(f"Nombre de Documents : {len(corpus.id2doc)}")
    print(f"Nombre d'Auteurs : {len(corpus.authors)}")
    print(f"Total de Caractères : {sum(len(doc.texte) for doc in corpus.id2doc.values())}")
    print(f"Total de Mots : {sum(len(doc.texte.split()) for doc in corpus.id2doc.values())}")
    print(f"Date du Plus Ancien Document : {min(doc.date for doc in corpus.id2doc.values())}")
    print(f"Date du Plus Récent Document : {max(doc.date for doc in corpus.id2doc.values())}")
    print("=========================")

# Fonction pour afficher les documents sous forme tabulaire
def afficher_documents(corpus, tri="date"):
    table = PrettyTable()
    table.field_names = ["ID", "Titre", "Auteur", "Date", "URL", "Nb Caractères"]

    # Tri des documents en fonction du critère choisi
    if tri == "date":
        documents = sorted(corpus.id2doc.values(), key=lambda x: x.date)
    elif tri == "titre":
        documents = sorted(corpus.id2doc.values(), key=lambda x: x.titre)
    elif tri == "auteur":
        documents = sorted(corpus.id2doc.values(), key=lambda x: x.auteur)
    else:
        documents = corpus.id2doc.values()

    # Ajout des documents à la table
    for doc_id, doc in enumerate(documents, start=1):
        table.add_row([
            doc_id,
            doc.titre[:30] + ("..." if len(doc.titre) > 30 else ""),  # Limiter la taille du titre
            doc.auteur[:15] + ("..." if len(doc.auteur) > 15 else ""),  # Limiter la taille de l'auteur
            doc.date,
            doc.url[:30] + ("..." if len(doc.url) > 30 else ""),  # Limiter l'URL
            len(doc.texte)
        ])
    print(table)

# Résumé du corpus
afficher_statistiques(corpus)

# Affichage des documents triés par date
afficher_documents(corpus, tri="date")

# Sauvegarde du corpus avec pickle
with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)  # Sauvegarder le corpus dans un fichier