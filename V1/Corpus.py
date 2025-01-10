from Classes import Author  # Importation de la classe Author pour gérer les auteurs dans le corpus
from datetime import datetime  # Importation de datetime pour gérer les dates
from Classes import Document, NewsDocument, ArxivDocument  # Importation des classes Document, NewsDocument, ArxivDocument

# Singleton pour la classe Corpus
class Corpus:
    _instance = None  # Déclaration de l'instance unique (Singleton)

    def __new__(cls, nom, *args, **kwargs):  # Méthode de création de l'instance unique
        if not cls._instance:  # Si aucune instance n'existe encore
            cls._instance = super(Corpus, cls).__new__(cls, *args, **kwargs)  # Créer l'instance unique
            cls._instance.init_singleton(nom)  # Initialisation de l'instance avec un nom
        return cls._instance  # Retourner l'instance unique

    def init_singleton(self, nom):  # Méthode d'initialisation de l'instance unique
        self.nom = nom  # Le nom du corpus
        self.authors = {}  # Dictionnaire pour stocker les auteurs
        self.aut2id = {}  # Dictionnaire pour associer un auteur à un identifiant
        self.id2doc = {}  # Dictionnaire pour associer un identifiant de document à un document
        self.ndoc = 0  # Nombre de documents dans le corpus
        self.naut = 0  # Nombre d'auteurs dans le corpus

    def add(self, doc):  # Méthode pour ajouter un document au corpus
        if doc.auteur not in self.aut2id:  # Si l'auteur du document n'est pas encore dans le corpus
            self.naut += 1  # Incrémenter le nombre d'auteurs
            self.authors[self.naut] = {"name": doc.auteur, "documents": []}  # Ajouter l'auteur au dictionnaire
            self.aut2id[doc.auteur] = self.naut  # Associer l'auteur à son identifiant
        self.authors[self.aut2id[doc.auteur]]["documents"].append(doc)  # Ajouter le document à l'auteur
        self.ndoc += 1  # Incrémenter le nombre de documents
        self.id2doc[self.ndoc] = doc  # Associer le document à un identifiant unique

    def get_documents(self, tri="abc"):  # Méthode pour récupérer les documents du corpus avec un critère de tri
        docs = list(self.id2doc.values())  # Convertir les documents en liste
        if tri == "abc":  # Si le tri est par titre alphabétique
            docs = sorted(docs, key=lambda x: x.titre.lower())  # Trier par titre
        elif tri == "123":  # Si le tri est par date
            docs = sorted(docs, key=lambda x: x.date)  # Trier par date
        return docs  # Retourner la liste triée des documents

    def show(self, n_docs=-1, tri="abc"):  # Méthode pour afficher les documents
        docs = self.get_documents(tri)  # Récupérer les documents triés
        if n_docs > 0:  # Si un nombre de documents est spécifié
            docs = docs[:n_docs]  # Limiter le nombre de documents à afficher
        print("\n".join(map(repr, docs)))  # Afficher les documents en utilisant leur représentation

    def __repr__(self):  # Méthode pour la représentation en chaîne du corpus
        docs = self.get_documents("abc")  # Récupérer les documents triés par titre
        return "\n".join(map(str, docs))  # Retourner une chaîne contenant les documents

    def __str__(self):  # Méthode pour la représentation en chaîne plus lisible du corpus
        return f"Corpus '{self.nom}' avec {self.ndoc} documents et {self.naut} auteurs."  # Affichage du nom, nombre de documents et d'auteurs

# Patron de conception Factory pour générer des documents
class DocumentFactory:
    @staticmethod
    def create_document(doc_type, titre, auteur, date, url, texte, extra=None):  # Méthode statique pour créer des documents
        if doc_type == "News":  # Si le type de document est "News"
            return NewsDocument(titre, auteur, date, url, texte, extra)  # Retourner un document News
        elif doc_type == "Arxiv":  # Si le type de document est "Arxiv"
            return ArxivDocument(titre, auteur, date, url, texte, extra)  # Retourner un document Arxiv
        else:  # Si le type de document est inconnu
            raise ValueError("Type de document inconnu")  # Lever une erreur