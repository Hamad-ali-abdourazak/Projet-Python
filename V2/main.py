import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SearchEngine import SearchEngine
from Corpus import Corpus

# Charger le corpus
corpus = Corpus.load("corpus.pkl")

# Créer le moteur de recherche
search_engine = SearchEngine(corpus)

# Demander à l'utilisateur d'entrer une requête
query = input("Entrez votre requête : ")

# Effectuer la recherche
results = search_engine.search(query, top_n=10)

# Afficher les résultats
print("Résultats de la recherche :")
for index, row in results.iterrows():
    print(f"Document: {row['Document']}\nScore: {row['Score']}\n")