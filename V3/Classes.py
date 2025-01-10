from datetime import datetime  # Importation de la classe datetime pour gérer les dates

# Classe représentant un document générique
class Document:
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre  # Initialisation du titre du document
        self.auteur = auteur  # Initialisation de l'auteur du document
        # Conversion de la date sous forme de chaîne en un objet datetime si la date est une chaîne
        self.date = datetime.strptime(date, '%B %d, %Y') if isinstance(date, str) else date
        self.url = url  # Initialisation de l'URL du document
        self.texte = texte  # Initialisation du texte du document
        self.type = "Document"  # Champ pour stocker le type du document (sera défini dans les classes enfants)

    def afficher(self):
        # Retourne une chaîne résumant les informations du document, incluant le texte tronqué
        return f"Titre: {self.titre}, Auteur: {self.auteur}, Date: {self.date.strftime('%Y-%m-%d')}, URL: {self.url}, Texte: {self.texte[:50]}..."

    def __repr__(self):
        # Retourne une représentation du document avec tous ses attributs principaux
        return f"Document(titre={self.titre}, auteur={self.auteur}, date={self.date}, url={self.url}, texte={self.texte[:50]}...)"

# Classe représentant un document de type News
class NewsDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, source):
        super().__init__(titre, auteur, date, url, texte)  # Appel du constructeur de la classe parente (Document)
        self.source = source  # Initialisation de la source spécifique aux news
        self.type = "News"  # Définition du type de document

    def __repr__(self):
        # Retourne une représentation du document News avec tous ses attributs principaux
        return f"NewsDocument(titre={self.titre}, auteur={self.auteur}, date={self.date}, url={self.url}, texte={self.texte[:50]}..., source={self.source})"

# Classe représentant un document de type Arxiv
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, category):
        super().__init__(titre, auteur, date, url, texte)  # Appel du constructeur de la classe parente (Document)
        self.category = category  # Initialisation de la catégorie spécifique aux documents Arxiv
        self.type = "Arxiv"  # Définition du type de document

    def __repr__(self):
        # Retourne une représentation du document Arxiv avec tous ses attributs principaux
        return f"ArxivDocument(titre={self.titre}, auteur={self.auteur}, date={self.date}, url={self.url}, texte={self.texte[:50]}..., category={self.category})"

# Classe représentant un auteur
class Author:
    def __init__(self, name):
        # Initialisation de l'auteur avec son nom
        self.name = name
        self.ndoc = 0  # Nombre de documents produits par cet auteur
        self.production = {}  # Dictionnaire des productions de l'auteur (clé : titre, valeur : document)

    def add(self, document):
        # Ajoute un document à la production de l'auteur
        self.ndoc += 1  # Incrémente le nombre de documents produits
        self.production[document.titre] = document  # Associe le document au titre de l'auteur

    def get_productions(self):
        # Retourne la liste des documents produits par cet auteur
        return list(self.production.values())

    def __repr__(self):
        # Retourne une représentation détaillée de l'auteur avec le nombre de productions
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"

    def __str__(self):
        # Retourne une représentation concise de l'auteur avec son nom et le nombre de documents produits
        return f"Auteur: {self.name}, Nombre de documents: {self.ndoc}"