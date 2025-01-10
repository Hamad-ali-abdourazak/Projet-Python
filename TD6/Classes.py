import datetime

class Document:
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = datetime.datetime.strptime(date, '%Y/%m/%d') if isinstance(date, str) else date
        self.url = url
        self.texte = texte
        self.type = "Document"

    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date.strftime('%Y-%m-%d')}\tURL : {self.url}\tTexte : {self.texte[:50]}..."

    def __str__(self):
        return f"{self.titre}, par {self.auteur}"

    def getType(self):
        return self.type

class NewsDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, source):
        super().__init__(titre, auteur, date, url, texte)
        self.source = source
        self.type = "News"

    def __str__(self):
        return f"NewsDocument: {self.titre} by {self.auteur} from {self.source} on {self.date}"

    def getType(self):
        return self.type

class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs
        self.type = "Arxiv"

    def get_co_auteurs(self):
        return self.co_auteurs

    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs

    def __str__(self):
        co_auteurs_str = ", ".join(self.co_auteurs)
        return f"{super().__str__()} avec co-auteurs : {co_auteurs_str}"

class Author:
    def __init__(self, name):
        self.name = name
        self.documents = []

    def add(self, document):
        self.documents.append(document)

    def __str__(self):
        return f"Author: {self.name} with {len(self.documents)} documents"