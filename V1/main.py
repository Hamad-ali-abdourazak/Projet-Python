import urllib.request
import xmltodict
import datetime
from Classes import Document, Author
from Corpus import Corpus
import pickle
from prettytable import PrettyTable
import requests
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)

def fetch_newsapi_articles(api_key, query, limit=100):
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
            contenu = article['content'].replace("\n", " ").strip() if article['content'] else titre
            auteur = article['author'] if article['author'] else "Auteur Inconnu"
            date = article['publishedAt'] if 'publishedAt' in article else "2023-01-01T00:00:00Z"
            articles.append((titre, contenu, auteur, date))
        
        return articles

    except Exception as e:
        logging.error(f"Erreur NewsAPI: {e}")
        return []

def fetch_arxiv_articles(query, max_results=50):
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
            contenu = entry['summary'].replace("\n", " ").strip()
            auteurs = [author['name'] for author in entry['author']] if isinstance(entry['author'], list) else [entry['author']['name']]
            date = entry['published'] if 'published' in entry else "2023-01-01T00:00:00Z"
            articles.append((titre, contenu, tuple(auteurs), date))
        return articles
    except Exception as e:
        logging.error(f"Erreur Arxiv: {e}")
        return []

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

def afficher_documents(corpus, tri="date"):
    table = PrettyTable()
    table.field_names = ["ID", "Titre", "Auteur", "Date", "URL", "Nb Caractères"]

    if tri == "date":
        documents = sorted(corpus.id2doc.values(), key=lambda x: x.date)
    elif tri == "titre":
        documents = sorted(corpus.id2doc.values(), key=lambda x: x.titre)
    elif tri == "auteur":
        documents = sorted(corpus.id2doc.values(), key=lambda x: x.auteur)
    else:
        documents = corpus.id2doc.values()

    for doc_id, doc in enumerate(documents, start=1):
        auteur_str = ", ".join(doc.auteur) if isinstance(doc.auteur, tuple) else doc.auteur
        table.add_row([
            doc_id,
            doc.titre[:30] + ("..." if len(doc.titre) > 30 else ""),
            auteur_str[:15] + ("..." if len(auteur_str) > 15 else ""),
            doc.date,
            doc.url[:30] + ("..." if len(doc.url) > 30 else ""),
            len(doc.texte)
        ])
    print(table)

# Récupération des documents depuis NewsAPI et Arxiv
newsapi_key = '3bef90d88eff47159c895ef3ff77f92a'
corpus_newsapi = fetch_newsapi_articles(newsapi_key, 'climate', limit=100)
corpus_arxiv = fetch_arxiv_articles('climate', max_results=50)

# Combiner les deux corpus
docs = corpus_newsapi + corpus_arxiv

# Supprimer les doublons
docs = list(set(tuple(doc) for doc in docs))

# Suppression des documents trop courts
for i, (titre, contenu, auteur, date) in enumerate(docs):
    if len(contenu) < 100:
        docs.remove((titre, contenu, auteur, date))

# Création d'une chaîne de texte avec tous les documents restants
longueChaineDeCaracteres = " ".join([contenu for titre, contenu, auteur, date in docs])

# Construction des objets Document à partir des données NewsAPI et ArXiv
collection = []
for titre, contenu, auteur, date in docs:
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    date_str = date_obj.strftime('%Y/%m/%d')
    document = Document(titre=titre, auteur=auteur, date=date_str, url="", texte=contenu)
    collection.append(document)

# Création d'un index des documents
id2doc = {i: doc.titre for i, doc in enumerate(collection)}

# Gestion des auteurs
authors = {}
aut2id = {}
num_auteurs_vus = 0

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

# Affichage des détails des documents
for i, doc in enumerate(collection):
    print(f"Document {i+1}\t# caractères : {len(doc.texte)}\t# mots : {len(doc.texte.split(' '))}\t# phrases : {len(doc.texte.split('.'))}")

# Résumé du corpus
afficher_statistiques(corpus)

# Affichage des documents triés par date
afficher_documents(corpus, tri="date")

# Sauvegarde du corpus avec pickle
with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)