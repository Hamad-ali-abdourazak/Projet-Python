from datetime import datetime  # Importation de la classe datetime pour gérer les dates

# Classe représentant un document générique
class Document:
    def __init__(self, titre, auteur=None, date=None, texte=None):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.texte = texte

    def __repr__(self):
        return f"Document(titre={self.titre}, auteur={self.auteur}, date={self.date}, texte={self.texte[:30]}...)"

# Classe représentant un document de type News
class NewsDocument(Document):
    def __init__(self, titre, auteur, date, texte, source):
        super().__init__(titre, auteur, date, texte)
        self.source = source

    def __repr__(self):
        return f"NewsDocument(titre={self.titre}, auteur={self.auteur}, date={self.date}, source={self.source})"

# Classe représentant un document de type Arxiv
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, texte, category):
        super().__init__(titre, auteur, date, texte)
        self.category = category

    def __repr__(self):
        return f"ArxivDocument(titre={self.titre}, auteur={self.auteur}, date={self.date}, category={self.category})"

# Classe représentant un auteur
class Author:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Author(name={self.name})"