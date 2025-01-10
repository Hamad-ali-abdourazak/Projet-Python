from datetime import datetime  # Importation de la classe datetime pour gérer les dates
class Document:
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre # Le titre du document
        self.auteur = auteur # L'auteur du document
        self.date = datetime.strptime(date, '%Y/%m/%d') if isinstance(date, str) else date # Conversion de la date de publication en objet datetime, si la date est fournie sous forme de chaîne
        self.url = url # L'URL du document
        self.texte = texte # Le contenu textuel du document


    def afficher(self):
        return f"Titre: {self.titre}, Auteur: {self.auteur}, Date: {self.date.strftime('%Y-%m-%d')}, URL: {self.url}, Texte: {self.texte[:50]}..."

    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date.strftime('%Y-%m-%d')}\tURL : {self.url}\tTexte : {self.texte[:50]}..."

    def __str__(self):
        return f"{self.titre}, par {self.auteur}"


class Author:
    def __init__(self, name):
        self.name = name  # Le nom de l'auteur
        self.ndoc = 0  # Nombre de documents produits par cet auteur
        self.production = {}  # Dictionnaire pour stocker les documents de l'auteur, avec leur titre comme clé

    def add(self, document):
       self.ndoc += 1  # Incrémente le compteur de documents de l'auteur
       self.production[document.titre] = document  # Ajoute le document dans le dictionnaire de production

    def get_productions(self):
        return list(self.production.values())

    def __repr__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"

    def __str__(self):
        return f"Auteur: {self.name}, Nombre de documents: {self.ndoc}"

